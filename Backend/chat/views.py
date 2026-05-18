import json
import urllib.error
import urllib.request

from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ChatConversacion, ChatMensaje
from .serializers import (
    ChatConversacionSerializer,
    ChatMensajeSerializer,
    EnviarMensajeSerializer,
)


def _construir_system_prompt(perfil):
    partes = [
        "Eres un coach fitness motivador, experto en entrenamiento y nutrición.",
        "Respondes en español, de forma concisa, práctica y cercana.",
        "Cuando tenga sentido, apóyate en los datos del usuario que aparecen a continuación.",
    ]

    partes.append(
        f"Usuario: {perfil.nombre} {perfil.apellido}, "
        f"{perfil.edad} años, {perfil.peso} kg, {perfil.altura} m."
    )

    try:
        from progress.models import Progreso
        progreso = (
            Progreso.objects
            .filter(usuario=perfil)
            .select_related("nivel", "rango")
            .first()
        )
        if progreso:
            nivel = progreso.nivel.numero if progreso.nivel else "?"
            rango = progreso.rango.nombre if progreso.rango else "?"
            partes.append(
                f"Progreso: nivel {nivel}, rango {rango}, "
                f"{progreso.xp_total} XP totales, "
                f"{progreso.entrenamientos} entrenamientos completados, "
                f"racha actual de {progreso.racha_actual} días."
            )
    except Exception:
        pass

    try:
        from workouts.models import Rutina
        rutinas = list(
            Rutina.objects.filter(usuario=perfil).values_list("nombre", flat=True)[:5]
        )
        if rutinas:
            partes.append("Sus rutinas guardadas: " + ", ".join(rutinas) + ".")
    except Exception:
        pass

    try:
        from nutrition.models import PlanNutricional
        planes = list(
            PlanNutricional.objects.filter(usuario=perfil).values_list("nombre", flat=True)[:5]
        )
        if planes:
            partes.append("Sus planes nutricionales: " + ", ".join(planes) + ".")
    except Exception:
        pass

    return " ".join(partes)


def _llamar_ollama(mensajes):
    url = settings.OLLAMA_URL.rstrip("/") + "/api/chat"
    payload = {
        "model": settings.OLLAMA_MODEL,
        "messages": mensajes,
        "stream": False,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return body.get("message", {}).get("content", "").strip()


class ChatConversacionViewSet(viewsets.ModelViewSet):
    queryset = ChatConversacion.objects.all()
    serializer_class = ChatConversacionSerializer

    def get_queryset(self):
        return ChatConversacion.objects.filter(
            usuario__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user.usuario)

    @action(detail=False, methods=["post"], url_path="enviar")
    def enviar(self, request):
        serializer = EnviarMensajeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        texto = serializer.validated_data["mensaje"]
        conversacion_id = serializer.validated_data.get("conversacion_id")

        perfil = request.user.usuario

        if conversacion_id:
            try:
                conversacion = ChatConversacion.objects.get(
                    pk=conversacion_id, usuario=perfil
                )
            except ChatConversacion.DoesNotExist:
                return Response(
                    {"detail": "Conversación no encontrada."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            conversacion = ChatConversacion.objects.create(
                usuario=perfil,
                titulo=texto[:100],
            )

        mensaje_usuario = ChatMensaje.objects.create(
            conversacion=conversacion,
            rol="user",
            contenido=texto,
        )

        historial = [{"role": "system", "content": _construir_system_prompt(perfil)}]
        for m in conversacion.chatmensaje_set.order_by("fecha"):
            role = "user" if m.rol == "user" else "assistant"
            historial.append({"role": role, "content": m.contenido})

        try:
            respuesta = _llamar_ollama(historial)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            return Response(
                {"detail": f"No se pudo contactar al modelo de IA: {e}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        if not respuesta:
            respuesta = "Lo siento, no pude generar una respuesta. Intenta de nuevo."

        mensaje_ia = ChatMensaje.objects.create(
            conversacion=conversacion,
            rol="ia",
            contenido=respuesta,
        )

        return Response({
            "conversacion_id": str(conversacion.id),
            "mensaje_usuario": ChatMensajeSerializer(mensaje_usuario).data,
            "mensaje_ia": ChatMensajeSerializer(mensaje_ia).data,
        })


class ChatMensajeViewSet(viewsets.ModelViewSet):
    queryset = ChatMensaje.objects.all()
    serializer_class = ChatMensajeSerializer

    def get_queryset(self):
        return ChatMensaje.objects.filter(
            conversacion__usuario__user=self.request.user
        )

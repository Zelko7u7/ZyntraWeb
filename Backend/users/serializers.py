from rest_framework import serializers
from .models import Usuario, Avatar
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Usuario
from progress.models import Progreso, Nivel, Rango


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    avatar = AvatarSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'email',
            'nombre',
            'apellido',
            'edad',
            'peso',
            'altura',
            'avatar',
            'created_at',
        ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    nombre = serializers.CharField(write_only=True)
    apellido = serializers.CharField(write_only=True)
    edad = serializers.IntegerField(write_only=True)
    peso = serializers.FloatField(write_only=True)
    altura = serializers.FloatField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'nombre', 'apellido', 'edad', 'peso', 'altura']

    def create(self, validated_data):
        nombre = validated_data.pop('nombre')
        apellido = validated_data.pop('apellido')
        edad = validated_data.pop('edad')
        peso = validated_data.pop('peso')
        altura = validated_data.pop('altura')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        # Guardamos la variable "usuario" para poder conectarla al progreso
        usuario_perfil = Usuario.objects.create(
            user=user,
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            peso=peso,
            altura=altura
        )

      
        nivel_base = Nivel.objects.filter(numero=1).first()
        rango_base = Rango.objects.filter(nombre='Principiante').first()

        # Creamos sus estadísticas en cero
        Progreso.objects.create(
            usuario=usuario_perfil,
            nivel=nivel_base,
            rango=rango_base,
            xp_total=0,
            racha_actual=0,
            mejor_racha=0,
            calorias_totales=0,
            entrenamientos=0
        )
        
        return user
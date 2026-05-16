import {
  Component,
  ElementRef,
  Input,
  Output,
  EventEmitter,
  ViewChild,
  AfterViewChecked,
  signal
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

export interface ChatMessage {
  rol: 'user' | 'ia';
  contenido: string;
  fecha: Date;
}

@Component({
  selector: 'app-chat-panel',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-panel.component.html',
  styleUrl: './chat-panel.component.scss'
})
export class ChatPanelComponent implements AfterViewChecked {
  @Input() abierto = false;
  @Output() cerrar = new EventEmitter<void>();

  @ViewChild('mensajesBox') private mensajesBox?: ElementRef<HTMLDivElement>;

  mensajeActual = '';
  enviando = signal<boolean>(false);
  mensajes = signal<ChatMessage[]>([
    {
      rol: 'ia',
      contenido:
        '¡Hola, atleta! 💪 Soy tu asistente fitness. Pregúntame por rutinas, nutrición o cómo mejorar tu progreso.',
      fecha: new Date()
    }
  ]);

  private debeHacerScroll = true;

  ngAfterViewChecked() {
    if (this.debeHacerScroll) {
      this.scrollAlFinal();
      this.debeHacerScroll = false;
    }
  }

  enviarMensaje() {
    const texto = this.mensajeActual.trim();
    if (!texto || this.enviando()) return;

    this.mensajes.update(m => [
      ...m,
      { rol: 'user', contenido: texto, fecha: new Date() }
    ]);
    this.mensajeActual = '';
    this.enviando.set(true);
    this.debeHacerScroll = true;

    // Respuesta simulada hasta tener backend IA
    setTimeout(() => {
      this.mensajes.update(m => [
        ...m,
        {
          rol: 'ia',
          contenido: this.generarRespuestaSimulada(texto),
          fecha: new Date()
        }
      ]);
      this.enviando.set(false);
      this.debeHacerScroll = true;
    }, 900);
  }

  cerrarPanel() {
    this.cerrar.emit();
  }

  private generarRespuestaSimulada(texto: string): string {
    const lower = texto.toLowerCase();
    if (lower.includes('rutina') || lower.includes('entren')) {
      return 'Te recomiendo empezar con una rutina full-body 3 días a la semana. Pronto podré sugerirte rutinas personalizadas según tu progreso.';
    }
    if (lower.includes('comida') || lower.includes('nutri') || lower.includes('dieta')) {
      return 'Para tus macros, prioriza proteína magra y carbohidratos complejos. Revisa la sección de Nutrición para ver tu plan asignado.';
    }
    if (lower.includes('hola') || lower.includes('buenas')) {
      return '¡Hola! ¿En qué puedo ayudarte hoy? Puedo hablarte de entrenamientos, nutrición o tu progreso.';
    }
    return 'Recibí tu mensaje. Pronto estaré conectado a un modelo de IA para responder con más detalle. ⚙️';
  }

  private scrollAlFinal() {
    if (!this.mensajesBox) return;
    const el = this.mensajesBox.nativeElement;
    el.scrollTop = el.scrollHeight;
  }
}

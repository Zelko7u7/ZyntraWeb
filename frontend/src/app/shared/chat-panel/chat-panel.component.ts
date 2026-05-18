import {
  AfterViewChecked,
  Component,
  ElementRef,
  EventEmitter,
  Input,
  Output,
  ViewChild,
  inject,
  signal,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

export interface ChatMessage {
  rol: 'user' | 'ia';
  contenido: string;
  fecha: Date;
}

interface EnviarResponse {
  conversacion_id: string;
  mensaje_usuario: { id: string; rol: string; contenido: string; fecha: string };
  mensaje_ia: { id: string; rol: string; contenido: string; fecha: string };
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
  @ViewChild('inputBox') private inputBox?: ElementRef<HTMLTextAreaElement>;

  private http = inject(HttpClient);
  private apiEnviar = 'http://localhost:8000/api/chat/chatconversacion/enviar/';

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

  mostrarBotonBajar = signal<boolean>(false);

  private conversacionId: string | null = null;
  private autoScrollPendiente = true;
  private estabaAlFinal = true;

  ngAfterViewChecked() {
    if (this.autoScrollPendiente && this.estabaAlFinal) {
      this.irAlFinal();
      this.autoScrollPendiente = false;
    }
  }

  enviarMensaje() {
    const texto = this.mensajeActual.trim();
    if (!texto || this.enviando()) return;

    this.estabaAlFinal = true;
    this.mensajes.update(m => [
      ...m,
      { rol: 'user', contenido: texto, fecha: new Date() }
    ]);
    this.mensajeActual = '';
    this.resetTextareaHeight();
    this.enviando.set(true);
    this.autoScrollPendiente = true;

    this.http.post<EnviarResponse>(this.apiEnviar, {
      mensaje: texto,
      conversacion_id: this.conversacionId,
    }).subscribe({
      next: (res) => {
        this.conversacionId = res.conversacion_id;
        this.mensajes.update(m => [
          ...m,
          {
            rol: 'ia',
            contenido: res.mensaje_ia.contenido,
            fecha: new Date(res.mensaje_ia.fecha),
          }
        ]);
        this.enviando.set(false);
        this.autoScrollPendiente = true;
      },
      error: (err) => {
        console.error(err);
        const detalle =
          err?.status === 503
            ? 'El modelo de IA todavía no está disponible. Si es la primera vez que levantas el contenedor, espera a que termine de descargarse (~2 GB).'
            : 'Hubo un problema al contactar al asistente. Intenta de nuevo en un momento.';
        this.mensajes.update(m => [
          ...m,
          { rol: 'ia', contenido: detalle, fecha: new Date() }
        ]);
        this.enviando.set(false);
        this.autoScrollPendiente = true;
      }
    });
  }

  cerrarPanel() {
    this.cerrar.emit();
  }

  onScroll() {
    if (!this.mensajesBox) return;
    const el = this.mensajesBox.nativeElement;
    const cercaDelFinal = el.scrollHeight - el.scrollTop - el.clientHeight < 80;
    this.estabaAlFinal = cercaDelFinal;
    this.mostrarBotonBajar.set(!cercaDelFinal);
  }

  irAlFinal() {
    if (!this.mensajesBox) return;
    const el = this.mensajesBox.nativeElement;
    el.scrollTop = el.scrollHeight;
    this.mostrarBotonBajar.set(false);
    this.estabaAlFinal = true;
  }

  autoResize() {
    const ta = this.inputBox?.nativeElement;
    if (!ta) return;
    ta.style.height = 'auto';
    const max = 160; // ~7 líneas
    ta.style.height = Math.min(ta.scrollHeight, max) + 'px';
  }

  onKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.enviarMensaje();
    }
  }

  private resetTextareaHeight() {
    const ta = this.inputBox?.nativeElement;
    if (ta) ta.style.height = 'auto';
  }
}

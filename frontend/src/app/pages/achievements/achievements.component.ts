import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

interface Logro {
  id?: string;
  nombre: string;
  xp: number;
  usuario?: string | null;
  desbloqueado?: boolean;
}

interface LogroUsuario {
  id: string;
  usuario: string;
  logro: string;
  logro_nombre: string;
  logro_xp: number;
  fecha: string;
}

interface LogroForm extends Logro {
  desbloquearAhora?: boolean;
}

@Component({
  selector: 'app-achievements',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './achievements.component.html',
  styleUrl: './achievements.component.scss'
})
export class AchievementsComponent implements OnInit {
  private http = inject(HttpClient);
  private apiLogros = 'http://localhost:8000/api/achievements/logro/';
  private apiLogrosUsuario = 'http://localhost:8000/api/achievements/logrousuario/';

  logros = signal<Logro[]>([]);
  logrosUsuario = signal<LogroUsuario[]>([]);
  errorMessage = signal<string>('');

  modalAbierto = signal<boolean>(false);
  editando = signal<boolean>(false);
  logroForm: LogroForm = this.logroVacio();

  ngOnInit() {
    this.cargarDatos();
  }

  cargarDatos() {
    this.http.get<any>(this.apiLogros).subscribe({
      next: (res) => this.logros.set(res.results || res),
      error: () => this.errorMessage.set('No se pudieron cargar los logros.')
    });

    this.http.get<any>(this.apiLogrosUsuario).subscribe({
      next: (res) => this.logrosUsuario.set(res.results || res),
      error: () => this.errorMessage.set('No se pudo cargar el historial de logros.')
    });
  }

  estaDesbloqueado(logroId: string): boolean {
    return this.logrosUsuario().some(lu => lu.logro === logroId);
  }

  // ============ CRUD ============
  abrirNuevoLogro() {
    this.logroForm = this.logroVacio();
    this.editando.set(false);
    this.errorMessage.set('');
    this.modalAbierto.set(true);
  }

  abrirEditarLogro(l: Logro) {
    this.logroForm = { ...l, desbloquearAhora: false };
    this.editando.set(true);
    this.errorMessage.set('');
    this.modalAbierto.set(true);
  }

  cerrarModal() {
    this.modalAbierto.set(false);
  }

  guardarLogro() {
    const data = {
      nombre: this.logroForm.nombre,
      xp: Number(this.logroForm.xp)
    };

    const peticion = this.editando()
      ? this.http.put<Logro>(`${this.apiLogros}${this.logroForm.id}/`, data)
      : this.http.post<Logro>(this.apiLogros, data);

    const desbloquearTrasCrear = !this.editando() && !!this.logroForm.desbloquearAhora;

    peticion.subscribe({
      next: (saved) => {
        if (desbloquearTrasCrear && saved?.id) {
          this.desbloquearLogro(saved, true);
        } else {
          this.cerrarModal();
          this.cargarDatos();
        }
      },
      error: (err) => {
        console.error(err);
        this.errorMessage.set('No se pudo guardar el logro.');
      }
    });
  }

  eliminarLogro(l: Logro) {
    if (!l.id) return;
    if (!confirm(`¿Eliminar el logro "${l.nombre}"?`)) return;
    this.http.delete(`${this.apiLogros}${l.id}/`).subscribe({
      next: () => this.cargarDatos(),
      error: (err) => {
        console.error(err);
        this.errorMessage.set('No se pudo eliminar el logro.');
      }
    });
  }

  // ============ Desbloquear / Bloquear ============
  desbloquearLogro(l: Logro, cerrarTras: boolean = false) {
    if (!l.id) return;
    this.http.post(`${this.apiLogros}${l.id}/unlock/`, {}).subscribe({
      next: () => {
        if (cerrarTras) this.cerrarModal();
        this.cargarDatos();
      },
      error: (err) => {
        console.error(err);
        this.errorMessage.set('No se pudo desbloquear el logro.');
      }
    });
  }

  bloquearLogro(l: Logro) {
    if (!l.id) return;
    this.http.post(`${this.apiLogros}${l.id}/lock/`, {}).subscribe({
      next: () => this.cargarDatos(),
      error: (err) => {
        console.error(err);
        this.errorMessage.set('No se pudo bloquear el logro.');
      }
    });
  }

  private logroVacio(): LogroForm {
    return { nombre: '', xp: 10, desbloquearAhora: true };
  }
}

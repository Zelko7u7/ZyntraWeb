import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

interface Rutina {
  id?: string;
  nombre: string;
  objetivo: string;
  nivel: string;
  duracion_min: number;
}

interface Entrenamiento {
  id?: string;
  rutina?: string | null;
  rutina_nombre?: string;
  fecha: string;
  duracion: number;
  calorias: number;
  estado: string;
}

@Component({
  selector: 'app-workouts',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './workouts.component.html',
  styleUrl: './workouts.component.scss'
})
export class WorkoutsComponent implements OnInit {
  private http = inject(HttpClient);
  private apiRutinas = 'http://localhost:8000/api/workouts/rutinas/';
  private apiEntrenamientos = 'http://localhost:8000/api/workouts/entrenamientos/';

  rutinas = signal<Rutina[]>([]);
  historial = signal<Entrenamiento[]>([]);
  errorMessage = signal<string>('');

  // Estado del modal de Rutina
  modalRutinaAbierto = signal<boolean>(false);
  editandoRutina = signal<boolean>(false);
  rutinaForm: Rutina = this.rutinaVacia();

  // Estado del modal de Entrenamiento
  modalEntrenamientoAbierto = signal<boolean>(false);
  editandoEntrenamiento = signal<boolean>(false);
  entrenamientoForm: Entrenamiento = this.entrenamientoVacio();

  ngOnInit() {
    this.cargarDatos();
  }

  cargarDatos() {
    this.http.get<any>(this.apiRutinas).subscribe({
      next: (res) => this.rutinas.set(res.results || res),
      error: () => this.errorMessage.set('No se pudieron cargar las rutinas.')
    });

    this.http.get<any>(this.apiEntrenamientos).subscribe({
      next: (res) => this.historial.set(res.results || res),
      error: () => this.errorMessage.set('No se pudo cargar el historial.')
    });
  }

  // ============ RUTINAS ============
  abrirNuevaRutina() {
    this.rutinaForm = this.rutinaVacia();
    this.editandoRutina.set(false);
    this.modalRutinaAbierto.set(true);
  }

  abrirEditarRutina(r: Rutina) {
    this.rutinaForm = { ...r };
    this.editandoRutina.set(true);
    this.modalRutinaAbierto.set(true);
  }

  cerrarModalRutina() {
    this.modalRutinaAbierto.set(false);
  }

  guardarRutina() {
    const data = {
      nombre: this.rutinaForm.nombre,
      objetivo: this.rutinaForm.objetivo,
      nivel: this.rutinaForm.nivel,
      duracion_min: Number(this.rutinaForm.duracion_min)
    };

    const peticion = this.editandoRutina()
      ? this.http.put(`${this.apiRutinas}${this.rutinaForm.id}/`, data)
      : this.http.post(this.apiRutinas, data);

    peticion.subscribe({
      next: () => {
        this.cerrarModalRutina();
        this.cargarDatos();
      },
      error: (err) => {
        console.error(err);
        this.errorMessage.set('No se pudo guardar la rutina.');
      }
    });
  }

  eliminarRutina(r: Rutina) {
    if (!confirm(`¿Eliminar la rutina "${r.nombre}"?`)) return;
    this.http.delete(`${this.apiRutinas}${r.id}/`).subscribe({
      next: () => this.cargarDatos(),
      error: (err) => {
        console.error(err);
        this.errorMessage.set('No se pudo eliminar la rutina.');
      }
    });
  }

  registrarEntrenamiento(rutina: Rutina) {
    const data = {
      rutina: rutina.id,
      fecha: new Date().toISOString(),
      duracion: rutina.duracion_min,
      calorias: Math.floor(Math.random() * (400 - 200 + 1)) + 200,
      estado: 'en_progreso'
    };

    this.http.post(this.apiEntrenamientos, data).subscribe({
      next: () => this.cargarDatos(),
      error: (err) => {
        console.error(err);
        this.errorMessage.set('No se pudo registrar el entrenamiento.');
      }
    });
  }

  cambiarEstado(entrenamiento: Entrenamiento, nuevoEstado: string) {
    if (!entrenamiento.id || entrenamiento.estado === nuevoEstado) return;

    const data = {
      rutina: entrenamiento.rutina,
      fecha: entrenamiento.fecha,
      duracion: entrenamiento.duracion,
      calorias: entrenamiento.calorias,
      estado: nuevoEstado
    };

    this.http.put(`${this.apiEntrenamientos}${entrenamiento.id}/`, data).subscribe({
      next: () => this.cargarDatos(),
      error: (err) => {
        console.error(err);
        this.errorMessage.set('No se pudo actualizar el estado.');
      }
    });
  }

  // ============ ENTRENAMIENTOS ============
  abrirEditarEntrenamiento(e: Entrenamiento) {
    this.entrenamientoForm = {
      ...e,
      fecha: this.toInputDate(e.fecha)
    };
    this.editandoEntrenamiento.set(true);
    this.modalEntrenamientoAbierto.set(true);
  }

  cerrarModalEntrenamiento() {
    this.modalEntrenamientoAbierto.set(false);
  }

  guardarEntrenamiento() {
    if (!this.entrenamientoForm.id) return;

    const data = {
      rutina: this.entrenamientoForm.rutina,
      fecha: new Date(this.entrenamientoForm.fecha).toISOString(),
      duracion: Number(this.entrenamientoForm.duracion),
      calorias: Number(this.entrenamientoForm.calorias),
      estado: this.entrenamientoForm.estado
    };

    this.http.put(`${this.apiEntrenamientos}${this.entrenamientoForm.id}/`, data).subscribe({
      next: () => {
        this.cerrarModalEntrenamiento();
        this.cargarDatos();
      },
      error: (err) => {
        console.error(err);
        this.errorMessage.set('No se pudo actualizar el entrenamiento.');
      }
    });
  }

  eliminarEntrenamiento(e: Entrenamiento) {
    if (!confirm('¿Eliminar este registro del historial?')) return;
    this.http.delete(`${this.apiEntrenamientos}${e.id}/`).subscribe({
      next: () => this.cargarDatos(),
      error: (err) => {
        console.error(err);
        this.errorMessage.set('No se pudo eliminar el entrenamiento.');
      }
    });
  }

  // ============ HELPERS ============
  private rutinaVacia(): Rutina {
    return { nombre: '', objetivo: '', nivel: '', duracion_min: 30 };
  }

  private entrenamientoVacio(): Entrenamiento {
    return {
      fecha: new Date().toISOString(),
      duracion: 0,
      calorias: 0,
      estado: 'en_progreso'
    };
  }

  private toInputDate(iso: string): string {
    // Convierte ISO a 'YYYY-MM-DDTHH:mm' para <input type="datetime-local">
    const d = new Date(iso);
    const pad = (n: number) => n.toString().padStart(2, '0');
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
  }

  nombreRutina(id: string | null | undefined): string {
    if (!id) return '—';
    return this.rutinas().find(r => r.id === id)?.nombre || '—';
  }
}

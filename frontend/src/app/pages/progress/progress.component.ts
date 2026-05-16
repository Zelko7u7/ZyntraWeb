import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

interface Nivel { id: string; numero: number; xp_requerida: number; }
interface Rango { id: string; nombre: string; xp_min: number; xp_max: number; }
interface Progreso {
  id: string;
  xp_total: number;
  racha_actual: number;
  mejor_racha: number;
  calorias_totales: number;
  entrenamientos: number;
  nivel: string; // ID
  rango: string; // ID
}

@Component({
  selector: 'app-progress',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './progress.component.html',
  styleUrl: './progress.component.scss'
})
export class ProgressComponent implements OnInit {
  private http = inject(HttpClient);

  progreso = signal<Progreso | null>(null);
  niveles = signal<Nivel[]>([]);
  rangos = signal<Rango[]>([]);

  // Calculamos el nivel actual y el progreso de la barra
  nivelActual = computed(() => {
    const p = this.progreso();
    if (!p) return null;
    return this.niveles().find(n => n.id === p.nivel);
  });

  rangoActual = computed(() => {
    const p = this.progreso();
    if (!p) return null;
    return this.rangos().find(r => r.id === p.rango);
  });

  porcentajeXP = computed(() => {
    const p = this.progreso();
    const n = this.nivelActual();
    if (!p || !n) return 0;
    return Math.min((p.xp_total / n.xp_requerida) * 100, 100);
  });

  ngOnInit() {
    this.cargarDatos();
  }

  cargarDatos() {
    // Cargar niveles para referencia
    this.http.get<any>('http://localhost:8000/api/progress/nivel/').subscribe({
      next: (res) => this.niveles.set(res.results || res)
    });

    // Cargar rangos para referencia
    this.http.get<any>('http://localhost:8000/api/progress/rango/').subscribe({
      next: (res) => this.rangos.set(res.results || res)
    });

    // Cargar el progreso del usuario logueado
    this.http.get<any>('http://localhost:8000/api/progress/progreso/').subscribe({
      next: (res) => {
        const data = res.results || res;
        this.progreso.set(data[0] || null); // Tomamos el primer registro de progreso
      }
    });
  }
}
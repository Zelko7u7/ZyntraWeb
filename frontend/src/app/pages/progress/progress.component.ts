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
  nivel: string;
  rango: string;
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

  nivelActual = computed(() => {
    const p = this.progreso();
    if (!p) return null;
    return this.niveles().find(n => n.id === p.nivel) || null;
  });

  rangoActual = computed(() => {
    const p = this.progreso();
    if (!p) return null;
    return this.rangos().find(r => r.id === p.rango) || null;
  });

  // El siguiente nivel después del actual (ordenado por xp_requerida)
  siguienteNivel = computed(() => {
    const actual = this.nivelActual();
    if (!actual) return null;
    const ordenados = [...this.niveles()].sort((a, b) => a.xp_requerida - b.xp_requerida);
    return ordenados.find(n => n.xp_requerida > actual.xp_requerida) || null;
  });

  // XP que se necesita para llegar al siguiente nivel
  xpMeta = computed(() => {
    return this.siguienteNivel()?.xp_requerida ?? this.nivelActual()?.xp_requerida ?? 0;
  });

  // Porcentaje progresivo dentro del nivel actual
  porcentajeXP = computed(() => {
    const p = this.progreso();
    const actual = this.nivelActual();
    const siguiente = this.siguienteNivel();
    if (!p || !actual) return 0;
    if (!siguiente) return 100;

    const baseXP = actual.xp_requerida;
    const metaXP = siguiente.xp_requerida;
    const rango = metaXP - baseXP;
    if (rango <= 0) return 100;

    const dentroDelNivel = p.xp_total - baseXP;
    return Math.min(Math.max((dentroDelNivel / rango) * 100, 0), 100);
  });

  ngOnInit() {
    this.cargarDatos();
  }

  cargarDatos() {
    this.http.get<any>('http://localhost:8000/api/progress/nivel/').subscribe({
      next: (res) => this.niveles.set(res.results || res)
    });

    this.http.get<any>('http://localhost:8000/api/progress/rango/').subscribe({
      next: (res) => this.rangos.set(res.results || res)
    });

    this.http.get<any>('http://localhost:8000/api/progress/progreso/').subscribe({
      next: (res) => {
        const data = res.results || res;
        this.progreso.set(data[0] || null);
      }
    });
  }
}

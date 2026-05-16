import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

interface PlanNutricional {
  id?: string;
  nombre: string;
  calorias: number;
  proteinas: number;
  carbs: number;
  grasas: number;
}

interface RegistroComida {
  id: string;
  fecha: string;
  calorias: number;
  proteinas: number;
  carbs: number;
  grasas: number;
  plan: string;
}

@Component({
  selector: 'app-nutrition',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './nutrition.component.html',
  styleUrl: './nutrition.component.scss'
})
export class NutritionComponent implements OnInit {
  private http = inject(HttpClient);
  private apiPlanes = 'http://localhost:8000/api/nutrition/plannutricional/';
  private apiRegistros = 'http://localhost:8000/api/nutrition/registrocomida/';

  planes = signal<PlanNutricional[]>([]);
  historial = signal<RegistroComida[]>([]);
  errorMessage = signal<string>('');

  modalAbierto = signal<boolean>(false);
  editando = signal<boolean>(false);
  planForm: PlanNutricional = this.planVacio();

  ngOnInit() {
    this.cargarDatos();
  }

  cargarDatos() {
    this.http.get<any>(this.apiPlanes).subscribe({
      next: (res) => this.planes.set(res.results || res),
      error: () => this.errorMessage.set('No se pudieron cargar los planes nutricionales.')
    });

    this.http.get<any>(this.apiRegistros).subscribe({
      next: (res) => {
        const data = res.results || res;
        const ordenado = data.sort((a: any, b: any) =>
          new Date(b.fecha).getTime() - new Date(a.fecha).getTime()
        );
        this.historial.set(ordenado);
      },
      error: () => this.errorMessage.set('No se pudo cargar la bitácora.')
    });
  }

  // ========== CRUD DE PLANES ==========
  abrirNuevoPlan() {
    this.planForm = this.planVacio();
    this.editando.set(false);
    this.modalAbierto.set(true);
  }

  abrirEditarPlan(p: PlanNutricional) {
    this.planForm = { ...p };
    this.editando.set(true);
    this.modalAbierto.set(true);
  }

  cerrarModal() {
    this.modalAbierto.set(false);
  }

  guardarPlan() {
    const data = {
      nombre: this.planForm.nombre,
      calorias: Number(this.planForm.calorias),
      proteinas: Number(this.planForm.proteinas),
      carbs: Number(this.planForm.carbs),
      grasas: Number(this.planForm.grasas)
    };

    const peticion = this.editando()
      ? this.http.put(`${this.apiPlanes}${this.planForm.id}/`, data)
      : this.http.post(this.apiPlanes, data);

    peticion.subscribe({
      next: () => {
        this.cerrarModal();
        this.cargarDatos();
      },
      error: (err) => {
        console.error(err);
        this.errorMessage.set('No se pudo guardar el plan.');
      }
    });
  }

  eliminarPlan(p: PlanNutricional) {
    if (!confirm(`¿Eliminar el plan "${p.nombre}"?`)) return;
    this.http.delete(`${this.apiPlanes}${p.id}/`).subscribe({
      next: () => this.cargarDatos(),
      error: (err) => {
        console.error(err);
        this.errorMessage.set('No se pudo eliminar el plan.');
      }
    });
  }

  // ========== REGISTRO DE COMIDA ==========
  registrarComida(plan: PlanNutricional) {
    const data = {
      plan: plan.id,
      fecha: new Date().toISOString(),
      calorias: plan.calorias,
      proteinas: plan.proteinas,
      carbs: plan.carbs,
      grasas: plan.grasas
    };

    this.http.post(this.apiRegistros, data).subscribe({
      next: () => this.cargarDatos(),
      error: (err) => {
        console.error(err);
        this.errorMessage.set('No se pudo registrar la comida.');
      }
    });
  }

  eliminarRegistro(r: RegistroComida) {
    if (!confirm('¿Eliminar este registro de la bitácora?')) return;
    this.http.delete(`${this.apiRegistros}${r.id}/`).subscribe({
      next: () => this.cargarDatos(),
      error: (err) => {
        console.error(err);
        this.errorMessage.set('No se pudo eliminar el registro.');
      }
    });
  }

  private planVacio(): PlanNutricional {
    return { nombre: '', calorias: 2000, proteinas: 150, carbs: 200, grasas: 70 };
  }
}

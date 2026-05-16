import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

interface PlanNutricional {
  id: string;
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
  plan: string; // ID del plan
}

@Component({
  selector: 'app-nutrition',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './nutrition.component.html',
  styleUrl: './nutrition.component.scss'
})
export class NutritionComponent implements OnInit {
  private http = inject(HttpClient);
  
  planes = signal<PlanNutricional[]>([]);
  historial = signal<RegistroComida[]>([]);

  ngOnInit() {
    this.cargarDatos();
  }

  cargarDatos() {
    // 1. Cargar Planes Disponibles
    this.http.get<any>('http://localhost:8000/api/nutrition/plannutricional/').subscribe({
      next: (response) => {
        const data = response.results ? response.results : response;
        this.planes.set(data);
      },
      error: (err) => console.error('Error al cargar planes:', err)
    });

    // 2. Cargar Historial del Usuario
    this.http.get<any>('http://localhost:8000/api/nutrition/registrocomida/').subscribe({
      next: (response) => {
        const data = response.results ? response.results : response;
        // Ordenamos el historial para que lo más reciente salga primero
        const historialOrdenado = data.sort((a: any, b: any) => 
          new Date(b.fecha).getTime() - new Date(a.fecha).getTime()
        );
        this.historial.set(historialOrdenado);
      },
      error: (err) => console.error('Error al cargar historial:', err)
    });
  }

  // Función para registrar una comida al hacer clic en un plan
  registrarComida(plan: PlanNutricional) {
    const nuevoRegistro = {
      plan: plan.id, // Pasamos el ID del plan seleccionado
      fecha: new Date().toISOString(), // Fecha y hora actual en formato compatible con Django
      calorias: plan.calorias,
      proteinas: plan.proteinas,
      carbs: plan.carbs,
      grasas: plan.grasas
    };

    this.http.post('http://localhost:8000/api/nutrition/registrocomida/', nuevoRegistro).subscribe({
      next: () => {
        alert('¡Comida registrada con éxito!');
        this.cargarDatos(); // Recargamos para actualizar el historial en pantalla
      },
      error: (err) => console.error('Error al registrar la comida:', err)
    });
  }
}
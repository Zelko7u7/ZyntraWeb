import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserService } from '../../services/user.service';
import { Usuario } from '../../models/usuario.model';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit {
  private userService = inject(UserService);

  perfil = signal<Usuario | null>(null);
  cargando = signal<boolean>(true);
  errorMessage = signal<string>('');

  ngOnInit() {
    this.userService.getMyProfile().subscribe({
      next: (data) => {
        this.perfil.set(data);
        this.cargando.set(false);
      },
      error: (err) => {
        console.error('Error al cargar perfil:', err);
        this.errorMessage.set('No se pudo cargar tu perfil. Intenta recargar la página.');
        this.cargando.set(false);
      }
    });
  }

  calcularIMC(peso: number, altura: number): string {
    if (!peso || !altura) return '--';
    const alturaMetros = altura > 3 ? altura / 100 : altura;
    const imc = peso / (alturaMetros * alturaMetros);
    return imc.toFixed(1);
  }

  iniciales(perfil: Usuario): string {
    const n = perfil.nombre?.charAt(0) ?? '';
    const a = perfil.apellido?.charAt(0) ?? '';
    return (n + a).toUpperCase() || perfil.username.charAt(0).toUpperCase();
  }
}

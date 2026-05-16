import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss'
})
export class RegisterComponent implements OnInit {
  private http = inject(HttpClient);
  private router = inject(Router);

  // Modelo con todos los datos necesarios para tu tabla Usuario
  registro = {
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    nombre: '',
    apellido: '',
    edad: null as number | null,
    peso: null as number | null,
    altura: null as number | null
  };

  errorMessage = '';

  ngOnInit() {
    // Verificamos si existe un token en el navegador (usuario ya logueado)
    if (typeof localStorage !== 'undefined' && localStorage.getItem('token')) {
      // Si ya está logueado, lo mandamos al login (o al home)
      this.router.navigate(['/login']); 
    }
  }

  onRegister() {
    // 1. Validamos que las contraseñas sean iguales
    if (this.registro.password !== this.registro.confirmPassword) {
      this.errorMessage = 'Las contraseñas no coinciden.';
      return;
    }

    // 2. Preparamos el paquete de datos completo para Django
    const payload = {
      username: this.registro.username,
      email: this.registro.email,
      password: this.registro.password,
      nombre: this.registro.nombre,
      apellido: this.registro.apellido,
      edad: this.registro.edad,
      peso: this.registro.peso,
      altura: this.registro.altura
    };

    // 3. Enviamos la petición al servidor
    this.http.post('http://localhost:8000/api/users/register/', payload).subscribe({
      next: () => {
        alert('¡Cuenta forjada con éxito! Ahora puedes iniciar sesión.');
        this.router.navigate(['/login']);
      },
      error: (err) => {
        console.error('Error completo:', err);
        // Extraemos y mostramos el mensaje exacto de error que nos manda Django
        if (err.error && typeof err.error === 'object') {
          const errores = Object.values(err.error).flat().join(' | ');
          this.errorMessage = `Error: ${errores}`;
        } else {
          this.errorMessage = 'Hubo un error al crear la cuenta. Revisa los datos e intenta de nuevo.';
        }
      }
    });
  }
}
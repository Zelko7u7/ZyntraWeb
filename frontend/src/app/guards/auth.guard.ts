import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  // Verificamos si existe el token guardado
  if (authService.getToken()) {
    return true; // el usuario está logueado, lo dejamos pasar
  }

  // Si no hay token, lo redirigimos a la pantalla de registro
  router.navigate(['/register']);
  return false; // bloqueamos el acceso a la ruta protegida
};
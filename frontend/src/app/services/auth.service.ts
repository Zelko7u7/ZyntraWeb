import { Injectable, inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private platformId = inject(PLATFORM_ID); // Identificador de la plataforma
  private apiUrl = 'http://localhost:8000/api/token/';

  login(username: string, password: string) {
    return this.http.post<any>(this.apiUrl, { username, password }).pipe(
      tap(response => {
        // solo guardamos si estamos en el navegador
        if (isPlatformBrowser(this.platformId)) {
          localStorage.setItem('access_token', response.access);
        }
      })
    );
  }

  getToken() {
    // solo leemos si estamos en el navegador, si no, devolvemos null
    if (isPlatformBrowser(this.platformId)) {
      return localStorage.getItem('access_token');
    }
    return null;
  }

  logout() {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem('access_token');
    }
  }
}
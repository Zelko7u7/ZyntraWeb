import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
// Importamos withFetch
import { provideHttpClient, withInterceptors, withFetch } from '@angular/common/http'; 
import { authInterceptor } from './interceptors/auth.interceptor';

import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes), 
    provideClientHydration(withEventReplay()),
    // Agregamos withFetch() aquí
    provideHttpClient(withFetch(), withInterceptors([authInterceptor])) 
  ]
};
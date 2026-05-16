import { Routes } from '@angular/router';
import { LayoutComponent } from './shared/layout/layout.component';
import { HomeComponent } from './pages/home/home.component';
import { AchievementsComponent } from './pages/achievements/achievements.component';
import { ChatComponent } from './pages/chat/chat.component';
import { NutritionComponent } from './pages/nutrition/nutrition.component';
import { ProgressComponent } from './pages/progress/progress.component';
import { WorkoutsComponent } from './pages/workouts/workouts.component';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component'; // 1. Importamos el componente
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  // RUTAS PÚBLICAS 
  { 
    path: 'login', 
    component: LoginComponent 
  },
  { 
    path: 'register', 
    component: RegisterComponent // 2. Agregamos la ruta aquí
  },

  // RUTAS PRIVADAS 
  {
    path: '',
    component: LayoutComponent,
    canActivate: [authGuard],
    children: [
      { path: '', component: HomeComponent },
      { path: 'achievements', component: AchievementsComponent },
      { path: 'chat', component: ChatComponent },
      { path: 'nutrition', component: NutritionComponent },
      { path: 'progress', component: ProgressComponent },
      { path: 'workouts', component: WorkoutsComponent },
    ]
  },
  
  // 3. Redirección por defecto si la ruta no existe (ahora apunta a register)
  { path: '**', redirectTo: 'register' } 
];
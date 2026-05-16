import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive, Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ChatPanelComponent } from '../chat-panel/chat-panel.component';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive, ChatPanelComponent],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss'
})
export class SidebarComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  chatAbierto = signal<boolean>(false);

  toggleChat() {
    this.chatAbierto.update(v => !v);
  }

  cerrarChat() {
    this.chatAbierto.set(false);
  }

  cerrarSesion() {
    this.authService.logout(); // Borra el token
    this.router.navigate(['/login']); // Lo manda al login
  }
}

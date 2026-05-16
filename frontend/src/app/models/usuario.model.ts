export interface Avatar {
  id: string;
  nombre: string;
  imagen: string | null;
}

export interface Usuario {
  id: string;
  username: string;
  email: string;
  nombre: string;
  apellido: string;
  edad: number;
  peso: number;
  altura: number;
  avatar: Avatar | null;
  created_at: string;
}

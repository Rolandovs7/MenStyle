import { Routes } from '@angular/router';

import { Login } from './pages/login/login';
import { Inicio } from './pages/inicio/inicio';
import { Registro } from './pages/registro/registro';
import { Usuarios } from './pages/usuarios/usuarios';
import { Permisos } from './pages/permisos/permisos';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    component: Login
  },
  {
    path: 'registro',
    component: Registro
  },
  {
    path: 'inicio',
    component: Inicio
  },
  {
    path: 'usuarios',
    component: Usuarios
  },
  { path: 'permisos', 
    component: Permisos 
  },
  {
    path: '**',
    redirectTo: 'login'
  }
  
];
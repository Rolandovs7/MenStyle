import { Component, inject, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  UsuariosService,
  Usuario,
  UsuarioActualizar
} from '../../core/services/usuarios.service';

@Component({
  selector: 'app-usuarios',
  imports: [CommonModule, FormsModule],
  templateUrl: './usuarios.html'
})
export class Usuarios implements OnInit {
  private usuariosService = inject(UsuariosService);
  private cdr = inject(ChangeDetectorRef);

  usuarios: Usuario[] = [];
  usuarioEditando: Usuario | null = null;
  error = '';
  mensaje = '';
  cargando = false;

  ngOnInit(): void {
    this.cargarUsuarios();
  }

  cargarUsuarios(): void {
    this.cargando = true;
    this.error = '';

    this.usuariosService.listar().subscribe({
      next: (usuarios) => {
        this.usuarios = usuarios;
        this.cargando = false;
        this.cdr.detectChanges();
      },
      error: (error) => {
        this.cargando = false;

        if (error.status === 401) {
          this.error = 'Sesión no válida. Inicia sesión nuevamente.';
        } else if (error.status === 403) {
          this.error = 'No tienes permisos de administrador.';
        } else {
          this.error = 'No se pudieron cargar los usuarios.';
        }
      }
    });
  }

  editar(usuario: Usuario): void {
    this.usuarioEditando = { ...usuario };
    this.error = '';
    this.mensaje = '';
  }

  cancelarEdicion(): void {
    this.usuarioEditando = null;
  }

  guardar(): void {
    if (!this.usuarioEditando) {
      return;
    }

    const datos: UsuarioActualizar = {
      nombre: this.usuarioEditando.nombre,
      apellido: this.usuarioEditando.apellido,
      email: this.usuarioEditando.email,
      activo: this.usuarioEditando.activo,
      rol: this.usuarioEditando.rol
    };

    this.usuariosService
      .actualizar(this.usuarioEditando.id, datos)
      .subscribe({
        next: (usuarioActualizado) => {
          const indice = this.usuarios.findIndex(
            u => u.id === usuarioActualizado.id
          );

          if (indice !== -1) {
            this.usuarios[indice] = usuarioActualizado;
          }

          this.usuarioEditando = null;
          this.mensaje = 'Usuario actualizado correctamente.';
        },
        error: (error) => {
          this.error =
            error.error?.detail ||
            'No se pudo actualizar el usuario.';
        }
      });
  }

  eliminar(usuario: Usuario): void {
    if (
      !confirm(
        `¿Seguro que deseas eliminar a ${usuario.nombre} ${usuario.apellido}?`
      )
    ) {
      return;
    }

    this.usuariosService.eliminar(usuario.id).subscribe({
      next: () => {
        this.usuarios = this.usuarios.filter(
          u => u.id !== usuario.id
        );

        this.mensaje = 'Usuario eliminado correctamente.';
      },
      error: (error) => {
        this.error =
          error.error?.detail ||
          'No se pudo eliminar el usuario.';
      }
    });
  }
}
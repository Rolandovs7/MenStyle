import { Component, ChangeDetectorRef, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PermisosService, Permiso } from '../../core/services/permisos.service';

@Component({
  selector: 'app-permisos',
  imports: [CommonModule, FormsModule],
  templateUrl: './permisos.html',
  styleUrl: './permisos.css'
})
export class Permisos implements OnInit {

  private permisosService = inject(PermisosService);
  private cdr = inject(ChangeDetectorRef);

  permisos: Permiso[] = [];
  permisosAsignados: number[] = [];

  rolSeleccionado = 'administrador';

  cargando = false;
  guardando = false;
  mensaje = '';
  error = '';

  ngOnInit(): void {
    this.cargarPermisos();
  }

  cargarPermisos(): void {
    this.cargando = true;
    this.error = '';

    this.permisosService.listar().subscribe({
      next: (permisos) => {
        this.permisos = permisos;
        this.cargarPermisosDelRol();
      },
      error: (error) => {
        console.error(error);
        this.error = 'No se pudieron cargar los permisos.';
        this.cargando = false;
        this.cdr.detectChanges();
      }
    });
  }

  cargarPermisosDelRol(): void {
    this.permisosService.porRol(this.rolSeleccionado).subscribe({
      next: (permisos) => {
        this.permisosAsignados = permisos.map(p => p.id);
        this.cargando = false;
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error(error);
        this.error = 'No se pudieron cargar los permisos del rol.';
        this.cargando = false;
        this.cdr.detectChanges();
      }
    });
  }

  cambiarRol(): void {
    this.mensaje = '';
    this.error = '';
    this.cargarPermisosDelRol();
  }

  tienePermiso(id: number): boolean {
    return this.permisosAsignados.includes(id);
  }

  cambiarPermiso(id: number): void {
    if (this.tienePermiso(id)) {
      this.permisosAsignados = this.permisosAsignados.filter(
        permisoId => permisoId !== id
      );
    } else {
      this.permisosAsignados = [
        ...this.permisosAsignados,
        id
      ];
    }
  }

  guardar(): void {
    this.guardando = true;
    this.mensaje = '';
    this.error = '';

    this.permisosService.porRol(this.rolSeleccionado).subscribe({
      next: (actuales) => {

        const actualesIds = actuales.map(p => p.id);

        const agregar = this.permisosAsignados.filter(
          id => !actualesIds.includes(id)
        );

        const quitar = actualesIds.filter(
          id => !this.permisosAsignados.includes(id)
        );

        let pendientes = agregar.length + quitar.length;

        if (pendientes === 0) {
          this.guardando = false;
          this.mensaje = 'Los permisos ya están actualizados.';
          this.cdr.detectChanges();
          return;
        }

        const terminado = () => {
          pendientes--;

          if (pendientes === 0) {
            this.guardando = false;
            this.mensaje = 'Permisos actualizados correctamente.';
            this.cdr.detectChanges();
          }
        };

        agregar.forEach(id => {
          this.permisosService.asignar(
            this.rolSeleccionado,
            id
          ).subscribe({
            next: terminado,
            error: (error) => {
              console.error(error);
              this.error = 'No se pudieron guardar algunos permisos.';
              terminado();
            }
          });
        });

        quitar.forEach(id => {
          this.permisosService.quitar(
            this.rolSeleccionado,
            id
          ).subscribe({
            next: terminado,
            error: (error) => {
              console.error(error);
              this.error = 'No se pudieron guardar algunos permisos.';
              terminado();
            }
          });
        });
      },
      error: (error) => {
        console.error(error);
        this.error = 'No se pudieron verificar los permisos actuales.';
        this.guardando = false;
        this.cdr.detectChanges();
      }
    });
  }
}
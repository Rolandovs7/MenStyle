import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import 'login_page.dart';

class HomePage extends StatelessWidget {
  final Map<String, dynamic> usuario;

  const HomePage({
    super.key,
    required this.usuario,
  });

  Future<void> cerrarSesion(BuildContext context) async {
    final authService = AuthService();

    authService.logout();

    if (!context.mounted) return;

    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(
        builder: (_) => const LoginPage(),
      ),
      (route) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        title: const Text(
          'MENSTYLE',
          style: TextStyle(
            fontWeight: FontWeight.w900,
            letterSpacing: 2,
          ),
        ),
        actions: [
          IconButton(
            tooltip: 'Cerrar sesión',
            icon: const Icon(Icons.logout),
            onPressed: () => cerrarSesion(context),
          ),
        ],
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 500),
            child: Card(
              elevation: 4,
              child: Padding(
                padding: const EdgeInsets.all(30),
                child: Column(
                  children: [
                    const Icon(Icons.person, size: 70),
                    const SizedBox(height: 20),
                    Text(
                      'Bienvenido, ${usuario['nombre']} 👋',
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        fontSize: 26,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 25),
                    ListTile(
                      leading: const Icon(Icons.person_outline),
                      title: const Text('Nombre'),
                      subtitle: Text(
                        '${usuario['nombre']} ${usuario['apellido']}',
                      ),
                    ),
                    ListTile(
                      leading: const Icon(Icons.email_outlined),
                      title: const Text('Correo'),
                      subtitle: Text('${usuario['email']}'),
                    ),
                    ListTile(
                      leading: const Icon(
                        Icons.admin_panel_settings_outlined,
                      ),
                      title: const Text('Rol'),
                      subtitle: Text('${usuario['rol']}'),
                    ),
                    const SizedBox(height: 25),
                    SizedBox(
                      width: double.infinity,
                      height: 50,
                      child: FilledButton.icon(
                        onPressed: () => cerrarSesion(context),
                        icon: const Icon(Icons.logout),
                        label: const Text('Cerrar sesión'),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
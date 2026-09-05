import 'dart:convert';
import 'package:http/http.dart' as http;

class AuthService {
  static final AuthService instance = AuthService._internal();

  factory AuthService() {
    return instance;
  }

  AuthService._internal();

  final String baseUrl = 'http://127.0.0.1:8000/api/auth';

  String? token;

  Future<String> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/login'),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: {
        'username': email,
        'password': password,
      },
    );

    if (response.statusCode != 200) {
      throw Exception('Error en login: ${response.body}');
    }

    final data = jsonDecode(response.body);

    token = data['access_token'];

    if (token == null) {
      throw Exception('El servidor no devolvió el token');
    }

    return token!;
  }

  Future<Map<String, dynamic>> obtenerUsuarioActual() async {
    if (token == null) {
      throw Exception('No existe token');
    }

    final response = await http.get(
      Uri.parse('$baseUrl/me'),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode != 200) {
      throw Exception(
        'Error obteniendo usuario: ${response.body}',
      );
    }

    return jsonDecode(response.body);
  }

  void logout() {
    token = null;
  }
}
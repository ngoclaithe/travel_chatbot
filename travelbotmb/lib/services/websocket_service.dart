import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class WebSocketService {
  WebSocketChannel? _channel;
  Timer? _pingTimer;

  bool _isConnecting = false;
  bool _isManualDisconnect = false;

  Function(String)? _onMessage;
  Function()? _onConnected;
  Function(String)? _onError;
  Function()? _onDisconnected;

  bool get isConnected => _channel != null;
  bool get isConnecting => _isConnecting;

  void connect({
    required Function(String) onMessage,
    required Function() onConnected,
    required Function(String) onError,
    Function()? onDisconnected,
  }) {
    _onMessage = onMessage;
    _onConnected = onConnected;
    _onError = onError;
    _onDisconnected = onDisconnected;

    _connectWebSocket();
  }

  void _connectWebSocket() {
    if (_isConnecting || _channel != null) {
      return;
    }

    _isConnecting = true;
    _isManualDisconnect = false;

    try {
      final socketUrl =
          dotenv.env['SOCKET_URL'] ?? 'ws://localhost:8000/ws/chat';

      _channel = WebSocketChannel.connect(Uri.parse(socketUrl));

      _channel!.ready
          .then((_) {
            _isConnecting = false;
            _onConnected?.call();
            _channel!.sink.add(jsonEncode({'type': 'init'}));
            _startPingTimer();
          })
          .catchError((error) {
            _isConnecting = false;
            _channel = null;
            _onError?.call('Khong the ket noi');
          });

      _channel!.stream.listen(
        _handleMessage,
        onError: _handleError,
        onDone: _handleDisconnect,
        cancelOnError: false,
      );
    } catch (e) {
      _isConnecting = false;
      _channel = null;
      _onError?.call('Khong the ket noi');
    }
  }

  void _handleMessage(dynamic message) {
    try {
      final data = jsonDecode(message);
      final type = data['type'] ?? '';

      if (type == 'ping') {
        _channel?.sink.add(jsonEncode({'type': 'pong'}));
        return;
      }

      if (type == 'init_ack') {
        return;
      }

      if (type == 'error') {
        _onError?.call(data['content'] ?? 'Loi tu server');
        return;
      }

      if (type == 'message') {
        _onMessage?.call(data['content'] ?? message.toString());
        return;
      }

      _onMessage?.call(data['content'] ?? message.toString());
    } catch (e) {
      _onMessage?.call(message.toString());
    }
  }

  void _handleError(error) {
    _isConnecting = false;
  }

  void _handleDisconnect() {
    _isConnecting = false;
    _stopPingTimer();
    _channel = null;
    _onDisconnected?.call();
  }

  void _startPingTimer() {
    _stopPingTimer();
    _pingTimer = Timer.periodic(const Duration(seconds: 30), (timer) {
      if (_channel != null) {
        try {
          _channel!.sink.add(jsonEncode({'type': 'ping'}));
        } catch (e) {
          timer.cancel();
        }
      }
    });
  }

  void _stopPingTimer() {
    _pingTimer?.cancel();
    _pingTimer = null;
  }

  void sendMessage(String message) {
    if (_channel == null) {
      return;
    }

    try {
      final data = jsonEncode({
        'type': 'message',
        'content': message,
        'timestamp': DateTime.now().toIso8601String(),
      });
      _channel!.sink.add(data);
    } catch (e) {
      _onError?.call('Khong the gui tin nhan');
    }
  }

  void disconnect() {
    _isManualDisconnect = true;
    _stopPingTimer();
    _channel?.sink.close();
    _channel = null;
    _isConnecting = false;
  }

  void retry() {
    disconnect();
    Future.delayed(const Duration(milliseconds: 500), () {
      _connectWebSocket();
    });
  }
}

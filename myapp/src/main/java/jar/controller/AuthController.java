package jar.controller;

import jar.dto.AuthResponse;
import jar.dto.LoginRequest;
import jar.dto.SignupRequest;
import jar.service.AuthService;

import lombok.RequiredArgsConstructor;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    // SIGNUP
    @PostMapping("/signup")
    public ResponseEntity<AuthResponse> signup(
            @RequestBody SignupRequest request) {

        return ResponseEntity.ok(
                authService.signup(request));
    }

    // LOGIN
    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(
            @RequestBody LoginRequest request) {

        return ResponseEntity.ok(
                authService.login(request));
    }
}
package jar.service;

import jar.dto.AuthResponse;
import jar.dto.LoginRequest;
import jar.dto.SignupRequest;
import jar.model.User;
import jar.repository.UserRepository;
import jar.security.JwtService;

import lombok.RequiredArgsConstructor;

import org.springframework.security.authentication.
        AuthenticationManager;

import org.springframework.security.authentication.
        UsernamePasswordAuthenticationToken;

import org.springframework.security.crypto.password.
        PasswordEncoder;

import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;

    private final PasswordEncoder passwordEncoder;

    private final JwtService jwtService;

    private final AuthenticationManager authenticationManager;

    // SIGNUP
    public AuthResponse signup(SignupRequest request) {

        // Check if email already exists
        if (userRepository.findByEmail(request.getEmail())
                .isPresent()) {

            throw new RuntimeException(
                    "Email already exists");
        }

        // Create user
        User user = new User();

        user.setName(request.getName());

        user.setEmail(request.getEmail());

        user.setPassword(
                passwordEncoder.encode(
                        request.getPassword()));

        user.setRole("USER");

        userRepository.save(user);

        // Generate JWT
        String token =
                jwtService.generateToken(user.getEmail());

        return new AuthResponse(
                token,
                "User registered successfully");
    }

    // LOGIN
    public AuthResponse login(LoginRequest request) {

        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        request.getEmail(),
                        request.getPassword()
                )
        );

        User user = userRepository
                .findByEmail(request.getEmail())
                .orElseThrow();

        String token =
                jwtService.generateToken(user.getEmail());

        return new AuthResponse(
                token,
                "Login successful");
    }
}
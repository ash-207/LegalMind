package jar.service;

import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;

import org.springframework.core.io.FileSystemResource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import jar.dto.TranscriptionApiResponse;
import jar.dto.TranscriptionResponse;
import jar.model.Transcription;
import jar.model.User;
import jar.repository.TranscriptionRepository;
import jar.repository.UserRepository;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class TranscriptionService {

    private final TranscriptionRepository repository;

    private final UserRepository userRepository;

    private final RestTemplate restTemplate;

    public TranscriptionResponse uploadAudio(
            MultipartFile file,
            String userEmail)
            throws IOException {

        // Create uploads folder
        String uploadDirectory =
                System.getProperty("user.dir")
                        + "/audio_uploads/";

        File directory =
                new File(uploadDirectory);

        if (!directory.exists()) {
            directory.mkdirs();
        }

        // File path
        String filePath =
                uploadDirectory
                        + file.getOriginalFilename();

        // Save file
        File destination =
                new File(filePath);

        file.transferTo(destination);

        // FastAPI URL
        String fastApiUrl =
                "http://127.0.0.1:8000/transcribe";

        // Multipart request body
        MultiValueMap<String, Object> body =
                new LinkedMultiValueMap<>();

        body.add(
                "file",
                new FileSystemResource(destination));

        // Headers
        HttpHeaders headers =
                new HttpHeaders();

        headers.setContentType(
                MediaType.MULTIPART_FORM_DATA);

        // Request entity
        HttpEntity<MultiValueMap<String, Object>>
                requestEntity =
                new HttpEntity<>(body, headers);

        // Call FastAPI
        ResponseEntity<TranscriptionApiResponse>
                response =
                restTemplate.postForEntity(
                        fastApiUrl,
                        requestEntity,
                        TranscriptionApiResponse.class);

        // Fetch user
        User user =
                userRepository
                        .findByEmail(userEmail)
                        .orElseThrow();

        // Create entity
        Transcription transcription =
                new Transcription();

        transcription.setFileName(
                file.getOriginalFilename());

        transcription.setFilePath(filePath);

        transcription.setTranscription(
                response.getBody()
                        .getTranscription());

        transcription.setUploadedAt(
                LocalDateTime.now());

        transcription.setUploadedBy(user);

        // Save to DB
        Transcription saved =
                repository.save(transcription);

        // Return response
        return TranscriptionResponse
                .builder()
                .id(saved.getId())
                .fileName(saved.getFileName())
                .transcription(saved.getTranscription())
                .uploadedAt(saved.getUploadedAt())
                .uploadedBy(
                        saved.getUploadedBy()
                                .getEmail())
                .build();
    }
}
package jar.controller;

import java.io.IOException;
import java.security.Principal;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import jar.dto.TranscriptionResponse;
import jar.service.TranscriptionService;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/Transcription")
@RequiredArgsConstructor
public class TranscriptionController {

    private final TranscriptionService service;

    @PostMapping("/upload")
    public ResponseEntity<TranscriptionResponse>
    uploadAudio(
            @RequestParam("file")
            MultipartFile file,
            Principal principal)
            throws IOException {

        TranscriptionResponse response =
                service.uploadAudio(
                        file,
                        principal.getName());

        return ResponseEntity.ok(response);
    }

    @GetMapping("/my-transcriptions")
public List<TranscriptionResponse>
getMyTranscriptions(
        Principal principal) {

    return service.getMyTranscriptions(
            principal.getName());
}
}
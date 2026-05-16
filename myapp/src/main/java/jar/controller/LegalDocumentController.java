package jar.controller;

import jar.dto.DocumentResponse;
import jar.service.LegalDocumentService;

import lombok.RequiredArgsConstructor;

import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/documents")
@RequiredArgsConstructor
public class LegalDocumentController {

    private final LegalDocumentService service;

    @PostMapping("/upload")
    public ResponseEntity<DocumentResponse>
    uploadDocument(
            @RequestParam("file")
            MultipartFile file,
            Authentication authentication) {

        try {

            String userEmail =
                    authentication.getName();

            DocumentResponse response =
                    service.uploadDocument(
                            file,
                            userEmail
                    );

            return ResponseEntity.ok(response);

        } catch (Exception e) {

            return ResponseEntity.badRequest()
                    .body(
                            DocumentResponse.builder()
                                    .summary(
                                            e.getMessage())
                                    .build()
                    );
        }
    }
}
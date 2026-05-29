package jar.service;

import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;
import java.util.List;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import jar.client.FastApiClient;
import jar.dto.DocumentResponse;
import jar.model.LegalDocument;
import jar.model.User;
import jar.repository.LegalDocumentRepository;
import jar.repository.UserRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class LegalDocumentService {

    private final LegalDocumentRepository repository;

    private final UserRepository userRepository;

    private final FastApiClient fastApiClient;

    public DocumentResponse uploadDocument(
            MultipartFile file,
            String userEmail)
            throws IOException {

// Absolute uploads directory
String uploadDirectory =
        System.getProperty("user.dir")
        + "/uploads/";

// Create folder if not exists
File directory =
        new File(uploadDirectory);

if (!directory.exists()) {
    directory.mkdirs();
}

// Full file path
String filePath =
        uploadDirectory
        + file.getOriginalFilename();

        // Save file
        File destination =
                new File(filePath);

        file.transferTo(destination);

        // Extract PDF text
        PDDocument pdf =
                PDDocument.load(destination);

        PDFTextStripper stripper =
                new PDFTextStripper();

        String extractedText =
                stripper.getText(pdf);

        pdf.close();

        // Fetch user
        User user = userRepository
                .findByEmail(userEmail)
                .orElseThrow();

        // Create document entity
        LegalDocument document =
                new LegalDocument();

        document.setTitle(
                file.getOriginalFilename());

        document.setFilePath(filePath);

        document.setOriginalText(extractedText);

        // Summary from ml_service FastAPI
       String summary =
        fastApiClient.generateSummary(
                extractedText
        );

        document.setSummary(summary);

        document.setUploadedAt(
                LocalDateTime.now());

        document.setUploadedBy(user);

        // Save to DB
        LegalDocument savedDocument =
                repository.save(document);

        // Return DTO
        return DocumentResponse.builder()
                .id(savedDocument.getId())
                .title(savedDocument.getTitle())
                .summary(savedDocument.getSummary())
                .uploadedAt(
                        savedDocument.getUploadedAt())
                .uploadedBy(
                        savedDocument
                                .getUploadedBy()
                                .getEmail())
                .build();
    }

    public List<DocumentResponse>
getMyDocuments(String email) {

    User user = userRepository
            .findByEmail(email)
            .orElseThrow();

    return repository
            .findByUploadedBy(user)
            .stream()
            .map(doc ->
                    DocumentResponse.builder()
                            .id(doc.getId())
                            .title(doc.getTitle())
                            .summary(doc.getSummary())
                            .uploadedAt(doc.getUploadedAt())
                            .uploadedBy(
                                    doc.getUploadedBy()
                                            .getEmail())
                            .build())
            .toList();
}
}
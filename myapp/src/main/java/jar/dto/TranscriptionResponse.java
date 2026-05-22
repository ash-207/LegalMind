package jar.dto;

import java.time.LocalDateTime;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TranscriptionResponse {

    private Long id;

    private String fileName;

    private String transcription;

    private LocalDateTime uploadedAt;

    private String uploadedBy;
}
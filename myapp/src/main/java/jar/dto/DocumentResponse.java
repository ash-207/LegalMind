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
public class DocumentResponse {

    private Long id;

    private String title;

    private String summary;

    private LocalDateTime uploadedAt;

    private String uploadedBy;
}
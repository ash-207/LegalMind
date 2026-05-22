package jar.model;

import java.time.LocalDateTime;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "audio_transcriptions")
@Data
public class Transcription {

     @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String fileName;

    private String filePath;

    @Column(columnDefinition = "TEXT")
    private String transcription;

    private LocalDateTime uploadedAt;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User uploadedBy;

    @PrePersist
    public void setUploadTime() {
        this.uploadedAt = LocalDateTime.now();
}

}
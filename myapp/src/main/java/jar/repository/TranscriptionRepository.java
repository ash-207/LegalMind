package jar.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import jar.model.Transcription;
import jar.model.User;

public interface TranscriptionRepository
        extends JpaRepository<Transcription, Long> {

                 List<Transcription>
    findByUploadedBy(User user);

}
package jar.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import jar.model.Transcription;

public interface TranscriptionRepository
        extends JpaRepository<Transcription, Long> {

}
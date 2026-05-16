package jar.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import jar.model.LegalDocument;

public interface LegalDocumentRepository
        extends JpaRepository<LegalDocument, Long> {
}
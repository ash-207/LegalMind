package jar.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import jar.model.LegalDocument;
import jar.model.User;
import java.util.List;

public interface LegalDocumentRepository
        extends JpaRepository<LegalDocument, Long> {
                List<LegalDocument>
    findByUploadedBy(User user);
}
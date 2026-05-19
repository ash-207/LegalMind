package jar.client;

import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import jar.dto.SummaryRequest;
import jar.dto.SummaryResponse;

@Component
public class FastApiClient {

    private final RestTemplate restTemplate =
            new RestTemplate();

    private static final String FASTAPI_URL =
            "http://127.0.0.1:8000/summarize";

    public String generateSummary(String text) {

        SummaryRequest request =
                new SummaryRequest(text);

        SummaryResponse response =
                restTemplate.postForObject(
                        FASTAPI_URL,
                        request,
                        SummaryResponse.class
                );

        return response.getSummary();
    }
}
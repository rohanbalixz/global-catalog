# ER Diagram

\`\`\`mermaid
erDiagram
    CATALOG_CLIENT ||--o{ CATALOG_ITEM : performs
    CATALOG_ITEM {
        string ItemID PK
        string Category
        int    Version
        string Name
    }
    AUDIT_LOG ||--o{ AUDIT_EVENT : logs
    AUDIT_EVENT {
        string EventID PK
        string ItemID FK
        string Timestamp
        string Action
        int    Version
    }
\`\`\`

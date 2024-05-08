CREATE TABLE IF NOT EXISTS position (
    position_id SERIAL PRIMARY KEY,
    position_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS company (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS currency (
    currency_id SERIAL PRIMARY KEY,
    currency_name VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS source (
    source_id SERIAL PRIMARY KEY,
    source_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS offer (
    offer_id SERIAL PRIMARY KEY,
    offer_id_internal VARCHAR(255),
    position_id INT,
    company_id INT,
    category_id INT,
    currency_id INT,
    source_id INT,
    link TEXT,
    seniority VARCHAR(50),
    salary_min DECIMAL(6, 2),
    salary_max DECIMAL(6, 2),

    FOREIGN KEY (position_id) REFERENCES position(position_id),
    FOREIGN KEY (company_id) REFERENCES company(company_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id),
    FOREIGN KEY (currency_id) REFERENCES currency(currency_id),
    FOREIGN KEY (source_id) REFERENCES source(source_id)
);

CREATE TABLE IF NOT EXISTS skills (
    skill_id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS offer_skills (
    offer_id INT,
    skill_id INT,
    FOREIGN KEY (offer_id) REFERENCES offer(offer_id),
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id),
    PRIMARY KEY (offer_id, skill_id)
);

CREATE TABLE ohlc_bar (
    id         BIGSERIAL    PRIMARY KEY,
    ticker     VARCHAR(20)  NOT NULL,
    "timestamp" TIMESTAMPTZ NOT NULL,
    open       DOUBLE PRECISION NOT NULL,
    high       DOUBLE PRECISION NOT NULL,
    low        DOUBLE PRECISION NOT NULL,
    close      DOUBLE PRECISION NOT NULL,
    volume     DOUBLE PRECISION NOT NULL,
    vwap       DOUBLE PRECISION,
    num_trades INTEGER,

    CONSTRAINT uq_ticker_timestamp UNIQUE (ticker, "timestamp")
);

CREATE INDEX ix_ticker_timestamp_desc ON ohlc_bar (ticker, "timestamp" DESC);

def dm_financial_performance():
    return """
    CREATE TABLE IF NOT EXISTS dm_financial_performance AS
    SELECT 
        ff.company_id,
        dc.shortName AS company_name,
        dm.market AS market_name,
        ff.Date AS reporting_date,
        ff.totalRevenue,
        ff.grossProfits,
        ff.ebitda,
        ff.returnOnAssets,
        ff.returnOnEquity,
        ff.debtToEquity,
        ff.currentRatio,
        ff.quickRatio,
        ff.earningsGrowth,
        ff.revenueGrowth
    FROM fact_financials ff
    JOIN dim_company dc ON ff.company_id = dc.company_id
    JOIN dim_market dm ON ff.market_id = dm.market_id;
    """

def dm_market_stock_performance():
    return """
    CREATE TABLE IF NOT EXISTS dm_market_stock_performance AS
    SELECT 
        ff.company_id,
        dc.shortName AS company_name,
        dm.market AS market_name,
        ff.Date AS reporting_date,
        ff.Open AS opening_price,
        ff.Close AS closing_price,
        ff.Volume AS trading_volume,
        dsp.fiftyTwoWeekHigh,
        dsp.fiftyTwoWeekLow,
        dsp.fiftyDayAverage,
        dsp.twoHundredDayAverage,
        dsp.trailingAnnualDividendRate,
        dsp.trailingAnnualDividendYield
    FROM fact_financials ff
    JOIN dim_company dc ON ff.company_id = dc.company_id
    JOIN dim_market dm ON ff.market_id = dm.market_id
    LEFT JOIN dim_stock_performance dsp ON ff.company_id = dsp.company_id;
    """  # Changed `ON ff.stock_id = dsp.stock_id` to `ON ff.company_id = dsp.company_id` for consistency.

def dm_dividend_investor_insights():
    return """
    CREATE TABLE IF NOT EXISTS dm_dividend_investor_insights AS
    SELECT 
        ff.company_id,
        dc.shortName AS company_name,
        dm.market AS market_name,
        ff.Date AS reporting_date,
        dd.dividendRate,
        dd.dividendYield,
        dd.exDividendDate,
        dd.payoutRatio,
        dd.fiveYearAvgDividendYield,
        dd.lastDividendValue,
        dd.lastDividendDate,
        ff.trailingPE,
        ff.forwardPE,
        ff.priceToBook,
        ff.priceEpsCurrentYear
    FROM fact_financials ff
    JOIN dim_company dc ON ff.company_id = dc.company_id
    JOIN dim_market dm ON ff.market_id = dm.market_id
    LEFT JOIN dim_dividends dd ON ff.company_id = dd.company_id;
    """  # Changed `ON ff.dividend_id = dd.dividend_id` to `ON ff.company_id = dd.company_id` for consistency.

def kpi_stock_performance():
    return """
    CREATE TABLE IF NOT EXISTS kpi_stock_performance AS
    SELECT 
        ff.company_id,
        ff.Date AS date,
        ff.marketCap AS market_cap,
        ff.enterpriseValue AS enterprise_value,
        (ff.Close - ff.previousClose) / NULLIF(ff.previousClose, 0) * 100 AS daily_return,
        (ff.High - ff.Low) / NULLIF(ff.Low, 0) * 100 AS intraday_volatility,
        ff.trailingPE AS trailing_pe_ratio,
        ff.forwardPE AS forward_pe_ratio
    FROM fact_financials ff;
    """

def kpi_financial_performance():
    return """
    CREATE TABLE IF NOT EXISTS kpi_financial_performance AS
    SELECT 
        ff.company_id,
        ff.Date AS date,
        ff.totalRevenue AS total_revenue,
        ff.grossProfits AS gross_profit,
        ff.ebitda AS ebitda,
        ((ff.totalRevenue - LAG(ff.totalRevenue) OVER (PARTITION BY ff.company_id ORDER BY ff.Date)) / 
            NULLIF(LAG(ff.totalRevenue) OVER (PARTITION BY ff.company_id ORDER BY ff.Date), 0)) * 100 AS revenue_growth_percent,
        ff.returnOnAssets AS return_on_assets,
        ff.returnOnEquity AS return_on_equity,
        ff.debtToEquity AS debt_to_equity,
        ff.currentRatio AS current_ratio,
        ff.quickRatio AS quick_ratio
    FROM fact_financials ff;
    """

def kpi_profitability():
    return """
    CREATE TABLE IF NOT EXISTS kpi_profitability AS
    SELECT 
        ff.company_id,
        ff.Date AS date,
        ff.ebitda AS ebitda,
        ff.returnOnAssets AS return_on_assets,
        ff.returnOnEquity AS return_on_equity,
        ff.earningsGrowth AS earnings_growth,
        ff.revenueGrowth AS revenue_growth,
        ff.priceToBook AS price_to_book_ratio,
        ff.priceEpsCurrentYear AS price_eps_current_year,
        ff.trailingPE AS trailing_pe_ratio,
        ff.forwardPE AS forward_pe_ratio
    FROM fact_financials ff;
    """

def kpi_price_volatility():
    return """
    CREATE TABLE IF NOT EXISTS kpi_price_volatility AS
    SELECT 
        ff.company_id,
        ff.Date AS date,
        ff.High AS daily_high,
        ff.Low AS daily_low,
        ((ff.High - ff.Low) / NULLIF(ff.Low, 0)) * 100 AS price_volatility_percent
    FROM fact_financials ff;
    """

def agg_financials_monthly():
    return """
    CREATE TABLE IF NOT EXISTS agg_financials_monthly AS
    SELECT 
        DATE_FORMAT(Date, '%Y-%m') AS month, 
        company_id,
        market_id,
        location_id,
        AVG(Open) AS avg_open,
        AVG(High) AS avg_high,
        AVG(Low) AS avg_low,
        AVG(Close) AS avg_close,
        SUM(Volume) AS total_volume,
        AVG(marketCap) AS avg_market_cap,
        AVG(enterpriseValue) AS avg_enterprise_value,
        AVG(totalRevenue) AS avg_total_revenue,
        AVG(grossProfits) AS avg_gross_profits,
        AVG(ebitda) AS avg_ebitda,
        AVG(returnOnAssets) AS avg_roa,
        AVG(returnOnEquity) AS avg_roe,
        AVG(debtToEquity) AS avg_debt_to_equity
    FROM fact_financials
    GROUP BY company_id, market_id, location_id, month;
    """

def agg_financials_quarterly():
    return """
    CREATE TABLE IF NOT EXISTS agg_financials_quarterly AS
    SELECT 
        CONCAT(YEAR(Date), '-Q', QUARTER(Date)) AS quarter,
        company_id,
        market_id,
        location_id,
        AVG(Open) AS avg_open,
        AVG(High) AS avg_high,
        AVG(Low) AS avg_low,
        AVG(Close) AS avg_close,
        SUM(Volume) AS total_volume,
        AVG(marketCap) AS avg_market_cap,
        AVG(enterpriseValue) AS avg_enterprise_value,
        AVG(totalRevenue) AS avg_total_revenue,
        AVG(grossProfits) AS avg_gross_profits,
        AVG(ebitda) AS avg_ebitda,
        AVG(returnOnAssets) AS avg_roa,
        AVG(returnOnEquity) AS avg_roe,
        AVG(debtToEquity) AS avg_debt_to_equity
    FROM fact_financials
    GROUP BY company_id, market_id, location_id, quarter;
    """

def agg_financials_annual():
    return """
    CREATE TABLE IF NOT EXISTS agg_financials_annual AS
    SELECT 
        YEAR(Date) AS year, 
        company_id,
        market_id,
        location_id,
        AVG(Open) AS avg_open,
        AVG(High) AS avg_high,
        AVG(Low) AS avg_low,
        AVG(Close) AS avg_close,
        SUM(Volume) AS total_volume,
        AVG(marketCap) AS avg_market_cap,
        AVG(enterpriseValue) AS avg_enterprise_value,
        AVG(totalRevenue) AS avg_total_revenue,
        AVG(grossProfits) AS avg_gross_profits,
        AVG(ebitda) AS avg_ebitda,
        AVG(returnOnAssets) AS avg_roa,
        AVG(returnOnEquity) AS avg_roe,
        AVG(debtToEquity) AS avg_debt_to_equity
    FROM fact_financials
    GROUP BY company_id, market_id, location_id, year;
    """
# auto-generated prompts modules per service
from .invoice import PROMPTS as INVOICE_PROMPTS
from .calendar import PROMPTS as CALENDAR_PROMPTS
from .table_analysis import PROMPTS as TABLE_ANALYSIS_PROMPTS
from .cargo_bl import PROMPTS as CARGO_BL_PROMPTS

SERVICE_PROMPTS = {
    'Invoice': INVOICE_PROMPTS,
    'Calendar': CALENDAR_PROMPTS,
    'Table Analysis': TABLE_ANALYSIS_PROMPTS,
    'Cargo_BL': CARGO_BL_PROMPTS,
}

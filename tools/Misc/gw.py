from dataclasses import dataclass

@dataclass
class OilSystem:
    production: float        # crude production (mbpd)
    crude_exports: float     # crude exports (mbpd)
    product_exports: float   # refined product exports (mbpd)
    imports: float           # total petroleum imports (mbpd)
    stock_change: float      # + build, - draw (mbpd equivalent)

    refinery_yield: float = 0.95  # simplified conversion efficiency

    def available_for_refining(self):
        return self.production - self.crude_exports + self.imports

    def product_supply(self):
        return self.available_for_refining() * self.refinery_yield

    def total_outflows(self):
        return self.crude_exports + self.product_exports

    def domestic_consumption(self):
        # mass balance closure
        return (
            self.available_for_refining()
            * self.refinery_yield
            - self.product_exports
            - self.stock_change
        )

    def check_balance(self):
        lhs = self.production + self.imports
        rhs = (
            self.crude_exports
            + self.product_exports
            + self.domestic_consumption()
            + self.stock_change
        )

        return {
            "lhs_total_supply": lhs,
            "rhs_total_demand": rhs,
            "difference": lhs - rhs
        }


# -------------------------
# Example scenario (edit freely)
# -------------------------

russia_like = OilSystem(
    production=10.0,
    crude_exports=5.0,
    product_exports=2.0,
    imports=0.0,
    stock_change=0.0
)

print("Available for refining:", russia_like.available_for_refining())
print("Domestic consumption (implied):", russia_like.domestic_consumption())
print("Balance check:", russia_like.check_balance())
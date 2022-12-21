Application contains:

IMS (Inventory Management System - Product app) -> Add/Modify Products
Client Management (Client App) -> Add/Create/Edit/View billing history
Invoice Generation (Invoice App) -> Allows the user to create an invoice that generates a PDF as well. 
Debit Payment Posting (Payment App) -> Once an invoice reaches a billed status either manually or via the Mailing automation users may post debits (payments) against the curr_amt_due of the invoice object until it reaches zero.
Mailing Automation (Mailing App (not currently implemeneted - Sprint scheduled for 1/23/22-1/27/22)) -> All invoices marked Ready to Bill in the database are emailed out with their PDF to the client associated to them.


Models(Tables):
Invoice -> fkey Business and client
InvoiceFile -> fkey Invoice
LineItems -> fkey Invoice
Client -> fkey Business
Business
Payment -> fkey Invoice
Product -> fkey Business
UserAssociations -> fkey Business and User

This is an active WIP -> all logic is subject to change.



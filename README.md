# Purchase RFQ Multi-Vendor Extension (Odoo 18)

This module extends the Odoo Purchase application to support a **multi-vendor RFQ process**, supplier bidding, and winning-bid selection.  
It was developed as part of an assignment demonstrating Odoo customization using Python, XML, and ORM inheritance.

---

##  Features Implemented

### 1️⃣ Assign an RFQ to Multiple Vendors
- Added a `Many2many` field **vendor_ids** on `purchase.order`.
- Allows selecting several vendors for the same RFQ.
- Added UI support to select multiple vendors on the RFQ form.

---

### 2️⃣ Supplier Bidding Module (`purchase.bid`)
- Created a new model `purchase.bid` with:
  - Vendor
  - RFQ
  - Bid state (Draft, Invited, Submitted, Accepted, Rejected)
  - Bid lines (product, quantity, price)
  - Total amount (computed)
- Added tree and form views for managing bids.
- Added menus and actions for procurement users.

---

### 3️⃣ Winning Bid Selection → Auto-Generate Purchase Order
- When a bid is marked as **Accepted**, the system automatically:
  - Creates a **Purchase Order** using bid lines.
  - Assigns the PO vendor as the selected winning vendor.

---

### 4️⃣ Purchase Request Module
- Added a new model where employees can submit **purchase requests**.
- Procurement department uses requests to generate RFQs.
- Forms and list views included.

---

## Module Structure 
purchase_rfq_multi_vendor/
│
├── models/
│ ├── purchase_order.py
│ ├── purchase_bid.py
│ └── purchase_request.py
│
├── views/
│ ├── purchase_bid_views.xml
│ ├── purchase_order_views.xml
│ └── purchase_request_views.xml
│
├── security/
│ ├── ir.model.access.csv
│
├── manifest.py
└── README.md 

---

## 🛠 Installation

1. Clone this repository into your Odoo custom addons directory:


2. Update Odoo module list:
   - Go to *Apps* → *Update Apps List*

3. Search for **Purchase RFQ Multi Vendor** and install it.

---

##  Usage Guide

### **Step 1 — Create a Purchase Request**
Employees submit purchase requests, which procurement converts into RFQs.

### **Step 2 — Create RFQ and Select Multiple Vendors**
Open RFQ → Choose several vendors from **Vendors** many2many field.

### **Step 3 — Send RFQ to Vendors**
The system generates a **Bid record** for each selected vendor.

### **Step 4 — Vendors Submit Bids**
Procurement enters bid line prices.

### **Step 5 — Accept Winning Bid**
Click **Accept Bid** → Automatically creates a Purchase Order.




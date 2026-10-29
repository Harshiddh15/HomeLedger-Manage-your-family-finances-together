-- Disable foreign key checks temporarily during data refresh
SET FOREIGN_KEY_CHECKS = 0;

-- 1. Clear old income, expenses, and udhar data
DELETE FROM income;
DELETE FROM expenses;
DELETE FROM udhar;

-- 2. Setup the 3 Families (id=1 Patel's Family, id=2 Rana's Family, id=3 Rathod's Family)
-- Password '123' hashed with BCrypt ($2a$11$OhB0g2ImfTKI6I7j4biJZuyNFy6APJB58jxGAv0G/81eBI4x/Bigq)
REPLACE INTO families (id, family_id, family_name, password, created_at) VALUES
(1, "Patel's Family", "Patel's Family", '$2a$11$OhB0g2ImfTKI6I7j4biJZuyNFy6APJB58jxGAv0G/81eBI4x/Bigq', '2026-10-01 00:00:00'),
(2, "Rana's Family", "Rana's Family", '$2a$11$OhB0g2ImfTKI6I7j4biJZuyNFy6APJB58jxGAv0G/81eBI4x/Bigq', '2026-10-01 00:00:00'),
(3, "Rathod's Family", "Rathod's Family", '$2a$11$OhB0g2ImfTKI6I7j4biJZuyNFy6APJB58jxGAv0G/81eBI4x/Bigq', '2026-10-01 00:00:00');

-- 3. Setup Members for each family
DELETE FROM members WHERE family_id IN (1, 2, 3);
INSERT INTO members (family_id, member_name, relation, mobile, Password) VALUES
(1, 'Father', 'Head', '9876543210', '123'),
(1, 'Mother', 'Wife', '9876543211', '123'),
(2, 'Father', 'Head', '9876543220', '123'),
(2, 'Mother', 'Wife', '9876543221', '123'),
(3, 'Father', 'Head', '9876543230', '123'),
(3, 'Mother', 'Wife', '9876543231', '123');

-- 4. Setup Categories for each family
DELETE FROM categories WHERE family_id IN (1, 2, 3);
INSERT INTO categories (family_id, name, type, icon, color) VALUES
-- Patel's Family
(1, 'Salary', 'Income', 'fa-money-bill-wave', '#11998e'),
(1, 'Mother\'s Income', 'Income', 'fa-briefcase', '#38ef7d'),
(1, 'Freelance', 'Income', 'fa-laptop-code', '#00e5ff'),
(1, 'Other Income', 'Income', 'fa-wallet', '#00b4d8'),
(1, 'Groceries', 'Expense', 'fa-cart-shopping', '#f59e0b'),
(1, 'Utilities', 'Expense', 'fa-bolt', '#ef4444'),
(1, 'Education', 'Expense', 'fa-graduation-cap', '#8b5cf6'),
(1, 'Transport', 'Expense', 'fa-car', '#06b6d4'),
(1, 'Medical', 'Expense', 'fa-heart-pulse', '#ec4899'),
(1, 'Other', 'Expense', 'fa-receipt', '#6b7280'),
-- Rana's Family
(2, 'Salary', 'Income', 'fa-money-bill-wave', '#11998e'),
(2, 'Mother\'s Income', 'Income', 'fa-briefcase', '#38ef7d'),
(2, 'Extra Work', 'Income', 'fa-laptop-code', '#00e5ff'),
(2, 'Additional Income', 'Income', 'fa-wallet', '#00b4d8'),
(2, 'Groceries', 'Expense', 'fa-cart-shopping', '#f59e0b'),
(2, 'Utilities', 'Expense', 'fa-bolt', '#ef4444'),
(2, 'Education', 'Expense', 'fa-graduation-cap', '#8b5cf6'),
(2, 'Transport', 'Expense', 'fa-car', '#06b6d4'),
(2, 'Medical', 'Expense', 'fa-heart-pulse', '#ec4899'),
(2, 'Other', 'Expense', 'fa-receipt', '#6b7280'),
-- Rathod's Family
(3, 'Salary', 'Income', 'fa-money-bill-wave', '#11998e'),
(3, 'Mother\'s Income', 'Income', 'fa-briefcase', '#38ef7d'),
(3, 'Extra Work', 'Income', 'fa-laptop-code', '#00e5ff'),
(3, 'Additional Income', 'Income', 'fa-wallet', '#00b4d8'),
(3, 'Groceries', 'Expense', 'fa-cart-shopping', '#f59e0b'),
(3, 'Utilities', 'Expense', 'fa-bolt', '#ef4444'),
(3, 'Education', 'Expense', 'fa-graduation-cap', '#8b5cf6'),
(3, 'Transport', 'Expense', 'fa-car', '#06b6d4'),
(3, 'Medical', 'Expense', 'fa-heart-pulse', '#ec4899'),
(3, 'Other', 'Expense', 'fa-receipt', '#6b7280');

-- 5. Insert Income Entries
-- Patel's Family (Total: ₹49,500)
INSERT INTO income (family_id, member_name, amount, source, date, description) VALUES
(1, 'Father', 25000.00, 'Salary', '2026-10-01', 'Father\'s salary'),
(1, 'Mother', 8000.00, 'Mother\'s Income', '2026-10-04', 'Mother\'s income'),
(1, 'Father', 3000.00, 'Freelance', '2026-10-08', 'Freelance work income'),
(1, 'Father', 12000.00, 'Salary', '2026-10-12', 'Salary received'),
(1, 'Father', 1500.00, 'Loan Repayment', '2026-10-20', 'Money received back from friend'),
(1, 'Mother', 0.00, 'Other Income', '2026-10-30', 'Small additional income');

-- Rana's Family (Total: ₹55,000)
INSERT INTO income (family_id, member_name, amount, source, date, description) VALUES
(2, 'Father', 30000.00, 'Salary', '2026-10-01', 'Father\'s salary'),
(2, 'Mother', 10000.00, 'Mother\'s Income', '2026-10-05', 'Mother\'s income'),
(2, 'Father', 5000.00, 'Extra Work', '2026-10-09', 'Extra work income'),
(2, 'Father', 8000.00, 'Salary', '2026-10-13', 'Salary received'),
(2, 'Mother', 2000.00, 'Additional Income', '2026-10-23', 'Additional income');

-- Rathod's Family (Total: ₹42,000)
INSERT INTO income (family_id, member_name, amount, source, date, description) VALUES
(3, 'Father', 22000.00, 'Salary', '2026-10-02', 'Father\'s salary'),
(3, 'Mother', 7000.00, 'Mother\'s Income', '2026-10-06', 'Mother\'s income'),
(3, 'Father', 3000.00, 'Extra Work', '2026-10-10', 'Extra work income'),
(3, 'Father', 8000.00, 'Salary', '2026-10-14', 'Salary received'),
(3, 'Mother', 2000.00, 'Additional Income', '2026-10-24', 'Additional income');

-- 6. Insert Expense Entries
-- Patel's Family (Total: ₹15,000)
INSERT INTO expenses (family_id, member_name, category, amount, date, description) VALUES
(1, 'Mother', 'Groceries', 2500.00, '2026-10-02', 'Grocery shopping'),
(1, 'Father', 'Utilities', 1500.00, '2026-10-06', 'Electricity bill'),
(1, 'Father', 'Education', 2000.00, '2026-10-10', 'School fees'),
(1, 'Father', 'Other', 3500.00, '2026-10-16', 'Money given to a friend'),
(1, 'Father', 'Transport', 1000.00, '2026-10-18', 'Transport expenses'),
(1, 'Mother', 'Medical', 2000.00, '2026-10-22', 'Medical expenses'),
(1, 'Mother', 'Other', 2500.00, '2026-10-28', 'Other household expenses');

-- Rana's Family (Total: ₹13,500)
INSERT INTO expenses (family_id, member_name, category, amount, date, description) VALUES
(2, 'Mother', 'Groceries', 3000.00, '2026-10-03', 'Grocery shopping'),
(2, 'Father', 'Utilities', 1800.00, '2026-10-07', 'Electricity and gas'),
(2, 'Father', 'Education', 2500.00, '2026-10-11', 'Education expenses'),
(2, 'Mother', 'Medical', 2200.00, '2026-10-15', 'Medical expenses'),
(2, 'Father', 'Transport', 1500.00, '2026-10-19', 'Transport expenses'),
(2, 'Mother', 'Other', 2500.00, '2026-10-29', 'Other expenses');

-- Rathod's Family (Total: ₹10,000)
INSERT INTO expenses (family_id, member_name, category, amount, date, description) VALUES
(3, 'Mother', 'Groceries', 2000.00, '2026-10-04', 'Grocery shopping'),
(3, 'Father', 'Utilities', 1200.00, '2026-10-08', 'Electricity bill'),
(3, 'Father', 'Education', 1500.00, '2026-10-12', 'Education expenses'),
(3, 'Mother', 'Medical', 1800.00, '2026-10-18', 'Medical expenses'),
(3, 'Father', 'Transport', 1000.00, '2026-10-26', 'Transport expenses'),
(3, 'Mother', 'Other', 2500.00, '2026-10-30', 'Other expenses');

-- 7. Insert Udhar Entries
-- Patel's Family:
-- Closing balances: Payable (Dene Hai): ₹17,500 | Receivable (Lene Hai): ₹2,000
INSERT INTO udhar (family_id, person_name, member_name, proof_image, type, amount, paid_amount, remaining_amount, reason, date, status) VALUES
(1, 'Grocery Store / Merchant', 'Mother', NULL, 'Dene Hai', 4500.00, 0.00, 4500.00, 'Grocery credit purchase', '2026-10-02', 'Pending'),
(1, 'Old Creditor / Local Vendor', 'Father', NULL, 'Dene Hai', 16000.00, 3000.00, 13000.00, 'Purana udhar (Old credit balance ₹3,000 paid)', '2026-10-18', 'Pending'),
(1, 'Friend (Rahul)', 'Father', NULL, 'Lene Hai', 3500.00, 1500.00, 2000.00, 'Friend ko udhar diya (₹1,500 repayment received)', '2026-10-12', 'Pending');

-- Rana's Family:
-- Closing balances: Payable (Dene Hai): ₹25,200 | Receivable (Lene Hai): ₹4,000
INSERT INTO udhar (family_id, person_name, member_name, proof_image, type, amount, paid_amount, remaining_amount, reason, date, status) VALUES
(2, 'Household Store', 'Mother', NULL, 'Dene Hai', 7000.00, 0.00, 7000.00, 'Household credit purchase', '2026-10-05', 'Pending'),
(2, 'Relative (Suresh)', 'Father', NULL, 'Lene Hai', 4000.00, 0.00, 4000.00, 'Relative ko udhar diya', '2026-10-15', 'Pending'),
(2, 'City Pharmacy', 'Mother', NULL, 'Dene Hai', 6200.00, 0.00, 6200.00, 'Medical credit purchase', '2026-10-21', 'Pending'),
(2, 'Old Creditor / Vendor', 'Father', NULL, 'Dene Hai', 9000.00, 2000.00, 7000.00, 'Purana udhar (Old credit repayment ₹2,000 paid)', '2026-10-26', 'Pending'),
(2, 'General Store', 'Father', NULL, 'Dene Hai', 5000.00, 0.00, 5000.00, 'Additional credit purchase', '2026-10-29', 'Pending');

-- Rathod's Family:
-- Closing balances: Payable (Dene Hai): ₹18,600 | Receivable (Lene Hai): ₹4,000
INSERT INTO udhar (family_id, person_name, member_name, proof_image, type, amount, paid_amount, remaining_amount, reason, date, status) VALUES
(3, 'Grocery Mart', 'Mother', NULL, 'Dene Hai', 5000.00, 0.00, 5000.00, 'Grocery credit purchase', '2026-10-09', 'Pending'),
(3, 'Neighbour (Amit)', 'Father', NULL, 'Lene Hai', 2500.00, 0.00, 2500.00, 'Neighbour ko udhar diya', '2026-10-16', 'Pending'),
(3, 'Former Associate', 'Father', NULL, 'Lene Hai', 1500.00, 0.00, 1500.00, 'Personal credit loan', '2026-10-01', 'Pending'),
(3, 'Home Appliances Store', 'Father', NULL, 'Dene Hai', 4000.00, 0.00, 4000.00, 'Household credit purchase', '2026-10-24', 'Pending'),
(3, 'Old Creditor / Supplier', 'Mother', NULL, 'Dene Hai', 11600.00, 2000.00, 9600.00, 'Purana udhar (Old credit repayment ₹2,000 paid)', '2026-10-30', 'Pending');

SET FOREIGN_KEY_CHECKS = 1;

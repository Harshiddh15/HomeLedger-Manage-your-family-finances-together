using FinanceManagementNet.Models;
using Microsoft.EntityFrameworkCore;

namespace FinanceManagementNet.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
        }

        public DbSet<Family> Families { get; set; }
        public DbSet<Member> Members { get; set; }
        public DbSet<Income> Incomes { get; set; }
        public DbSet<Expense> Expenses { get; set; }
        public DbSet<Udhar> Udhar { get; set; }
        public DbSet<Reminder> Reminders { get; set; }
        public DbSet<Budget> Budgets { get; set; }
        public DbSet<SavingsGoal> SavingsGoals { get; set; }
        public DbSet<RecurringExpense> RecurringExpenses { get; set; }
        public DbSet<Category> Categories { get; set; }
        public DbSet<RecurringIncome> RecurringIncomes { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configure Family entity
            modelBuilder.Entity<Family>(entity =>
            {
                entity.ToTable("families");
                entity.Property(e => e.Id).HasColumnName("id");
                entity.Property(e => e.FamilyId).HasColumnName("family_id");
                entity.Property(e => e.FamilyName).HasColumnName("family_name");
                entity.Property(e => e.Password).HasColumnName("password");
                entity.Property(e => e.CreatedAt).HasColumnName("created_at").HasDefaultValueSql("CURRENT_TIMESTAMP");
            });

            // Configure Member entity
            modelBuilder.Entity<Member>(entity =>
            {
                entity.ToTable("members");
                entity.Property(e => e.Id).HasColumnName("id");
                entity.Property(e => e.FamilyId).HasColumnName("family_id");
                entity.Property(e => e.MemberName).HasColumnName("member_name");
                entity.Property(e => e.Relation).HasColumnName("relation");
                entity.Property(e => e.Mobile).HasColumnName("mobile");
                entity.Property(e => e.ProfileImage).HasColumnName("profile_image");
                entity.HasOne(m => m.Family)
                      .WithMany(f => f.Members)
                      .HasForeignKey(m => m.FamilyId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // Configure Income entity
            modelBuilder.Entity<Income>(entity =>
            {
                entity.ToTable("income");
                entity.Property(e => e.Id).HasColumnName("id");
                entity.Property(e => e.FamilyId).HasColumnName("family_id");
                entity.Property(e => e.MemberName).HasColumnName("member_name");
                entity.Property(e => e.Amount).HasColumnName("amount");
                entity.Property(e => e.Source).HasColumnName("source");
                entity.Property(e => e.Date).HasColumnName("date");
                entity.Property(e => e.Description).HasColumnName("description");
                entity.HasOne(i => i.Family)
                      .WithMany(f => f.Incomes)
                      .HasForeignKey(i => i.FamilyId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // Configure Expense entity
            modelBuilder.Entity<Expense>(entity =>
            {
                entity.ToTable("expenses");
                entity.Property(e => e.Id).HasColumnName("id");
                entity.Property(e => e.FamilyId).HasColumnName("family_id");
                entity.Property(e => e.MemberName).HasColumnName("member_name");
                entity.Property(e => e.Category).HasColumnName("category");
                entity.Property(e => e.Amount).HasColumnName("amount");
                entity.Property(e => e.Description).HasColumnName("description");
                entity.Property(e => e.Date).HasColumnName("date");
                entity.HasOne(e => e.Family)
                      .WithMany(f => f.Expenses)
                      .HasForeignKey(e => e.FamilyId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // Configure Udhar entity
            modelBuilder.Entity<Udhar>(entity =>
            {
                entity.ToTable("udhar");
                entity.Property(e => e.Id).HasColumnName("id");
                entity.Property(e => e.FamilyId).HasColumnName("family_id");
                entity.Property(e => e.PersonName).HasColumnName("person_name");
                entity.Property(e => e.MemberName).HasColumnName("member_name");
                entity.Property(e => e.ProofImage).HasColumnName("proof_image");
                entity.Property(e => e.Type).HasColumnName("type");
                entity.Property(e => e.Amount).HasColumnName("amount");
                entity.Property(e => e.PaidAmount).HasColumnName("paid_amount").HasDefaultValue(0.00m);
                entity.Property(e => e.RemainingAmount).HasColumnName("remaining_amount");
                entity.Property(e => e.Reason).HasColumnName("reason");
                entity.Property(e => e.Date).HasColumnName("date");
                entity.Property(e => e.Status).HasColumnName("status").HasDefaultValue("Pending");
                entity.HasOne(u => u.Family)
                      .WithMany(f => f.Udhar)
                      .HasForeignKey(u => u.FamilyId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // Configure Reminder entity
            modelBuilder.Entity<Reminder>(entity =>
            {
                entity.ToTable("reminders");
                entity.Property(e => e.Id).HasColumnName("id");
                entity.Property(e => e.FamilyId).HasColumnName("family_id");
                entity.Property(e => e.Title).HasColumnName("title");
                entity.Property(e => e.Date).HasColumnName("date");
                entity.Property(e => e.Description).HasColumnName("description");
                entity.HasOne(r => r.Family)
                      .WithMany(f => f.Reminders)
                      .HasForeignKey(r => r.FamilyId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // Configure Budget entity
            modelBuilder.Entity<Budget>(entity =>
            {
                entity.ToTable("budgets");
                entity.Property(e => e.Id).HasColumnName("id");
                entity.Property(e => e.FamilyId).HasColumnName("family_id");
                entity.Property(e => e.Category).HasColumnName("category");
                entity.Property(e => e.Amount).HasColumnName("amount");
                entity.Property(e => e.Month).HasColumnName("month");
                entity.HasOne(b => b.Family)
                      .WithMany(f => f.Budgets)
                      .HasForeignKey(b => b.FamilyId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // Configure SavingsGoal entity
            modelBuilder.Entity<SavingsGoal>(entity =>
            {
                entity.ToTable("savings_goals");
                entity.Property(e => e.Id).HasColumnName("id");
                entity.Property(e => e.FamilyId).HasColumnName("family_id");
                entity.Property(e => e.GoalName).HasColumnName("goal_name");
                entity.Property(e => e.TargetAmount).HasColumnName("target_amount");
                entity.Property(e => e.CurrentAmount).HasColumnName("current_amount");
                entity.Property(e => e.TargetDate).HasColumnName("target_date");
                entity.Property(e => e.Description).HasColumnName("description");
                entity.HasOne(s => s.Family)
                      .WithMany(f => f.SavingsGoals)
                      .HasForeignKey(s => s.FamilyId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // Configure RecurringExpense entity
            modelBuilder.Entity<RecurringExpense>(entity =>
            {
                entity.ToTable("recurring_expenses");
                entity.Property(e => e.Id).HasColumnName("id");
                entity.Property(e => e.FamilyId).HasColumnName("family_id");
                entity.Property(e => e.MemberName).HasColumnName("member_name");
                entity.Property(e => e.Category).HasColumnName("category");
                entity.Property(e => e.Amount).HasColumnName("amount");
                entity.Property(e => e.Frequency).HasColumnName("frequency");
                entity.Property(e => e.DayOfMonth).HasColumnName("day_of_month");
                entity.Property(e => e.Description).HasColumnName("description");
                entity.Property(e => e.IsActive).HasColumnName("is_active");
                entity.HasOne(r => r.Family)
                      .WithMany(f => f.RecurringExpenses)
                      .HasForeignKey(r => r.FamilyId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // Configure Category entity
            modelBuilder.Entity<Category>(entity =>
            {
                entity.ToTable("categories");
                entity.Property(e => e.Id).HasColumnName("id");
                entity.Property(e => e.FamilyId).HasColumnName("family_id");
                entity.Property(e => e.Name).HasColumnName("name");
                entity.Property(e => e.Type).HasColumnName("type");
                entity.Property(e => e.Icon).HasColumnName("icon");
                entity.Property(e => e.Color).HasColumnName("color");
                entity.HasOne(c => c.Family)
                      .WithMany()
                      .HasForeignKey(c => c.FamilyId)
                      .OnDelete(DeleteBehavior.Cascade);
            });

            // Configure RecurringIncome entity
            modelBuilder.Entity<RecurringIncome>(entity =>
            {
                entity.ToTable("recurring_incomes");
                entity.Property(e => e.Id).HasColumnName("id");
                entity.Property(e => e.FamilyId).HasColumnName("family_id");
                entity.Property(e => e.MemberName).HasColumnName("member_name");
                entity.Property(e => e.Source).HasColumnName("source");
                entity.Property(e => e.Amount).HasColumnName("amount");
                entity.Property(e => e.Frequency).HasColumnName("frequency");
                entity.Property(e => e.DayOfMonth).HasColumnName("day_of_month");
                entity.Property(e => e.Description).HasColumnName("description");
                entity.Property(e => e.IsActive).HasColumnName("is_active");
                entity.HasOne(r => r.Family)
                      .WithMany(f => f.RecurringIncomes)
                      .HasForeignKey(r => r.FamilyId)
                      .OnDelete(DeleteBehavior.Cascade);
            });
        }
    }
}

using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;

namespace FinanceManagementNet.Filters
{
    public class AdminOnlyAttribute : ActionFilterAttribute
    {
        public override void OnActionExecuting(ActionExecutingContext context)
        {
            var session = context.HttpContext.Session;
            var familyDbId = session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                context.Result = new RedirectToActionResult("Login", "Account", null);
                return;
            }

            var loginType = session.GetString("LoginType");
            if (loginType != "Admin")
            {
                var controller = context.Controller as Controller;
                if (controller != null)
                {
                    controller.TempData["Error"] = "Admin function is locked. Member accounts do not have access to Admin controls.";
                }
                context.Result = new RedirectToActionResult("MemberDashboard", "Home", null);
                return;
            }

            base.OnActionExecuting(context);
        }
    }
}

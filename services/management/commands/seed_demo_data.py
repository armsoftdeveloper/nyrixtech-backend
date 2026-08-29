from django.core.management.base import BaseCommand
from services.models import Service, ServicePlan, FAQ, CaseStudy
from blog.models import BlogPost, BlogCategory


SERVICES = [
    ("IT Support", "managed-it", "LifeBuoy", "Responsive help desk and on-site support for your whole team.",
     ["Remote & on-site support", "Help desk ticketing", "Hardware procurement", "Employee onboarding/offboarding"]),
    ("Network Infrastructure", "network-infrastructure", "Network", "MikroTik routing, structured cabling, Wi-Fi and VPN.",
     ["MikroTik configuration", "VLAN segmentation", "Managed Wi-Fi", "Site-to-site VPN"]),
    ("Cybersecurity", "cybersecurity", "ShieldCheck", "Firewalls, endpoint protection and security audits.",
     ["Firewall management", "Endpoint protection", "Security audits", "Employee security training"]),
    ("Servers", "servers", "Server", "Windows Server, Linux and virtualization, managed end to end.",
     ["Windows Server administration", "Linux administration", "Virtualization", "Patch management"]),
    ("Backup", "backup", "DatabaseBackup", "Automated backup and tested disaster recovery.",
     ["Automated daily backups", "Offsite replication", "Disaster recovery planning", "Recovery testing"]),
    ("Monitoring", "monitoring", "Activity", "24/7 infrastructure monitoring with proactive alerting.",
     ["Zabbix-based monitoring", "Uptime alerting", "Capacity planning", "Monthly health reports"]),
    ("Cloud", "cloud", "Cloud", "Microsoft 365, Google Workspace and cloud infrastructure.",
     ["Microsoft 365 administration", "Google Workspace administration", "Cloud migration", "Cost optimization"]),
    ("Automation", "automation", "Workflow", "Infrastructure and AI-driven automation to cut manual work.",
     ["Infrastructure as code", "Automated provisioning", "AI-assisted operations", "Custom integrations"]),
]

PLANS = [
    ("Starter", "starter", "For small offices getting their first real IT support.", 149000, False,
     ["Up to 15 devices", "Remote help desk", "Monthly health checks", "Basic backup monitoring"], False),
    ("Business", "business", "For growing companies that need proactive management.", 349000, False,
     ["Up to 60 devices", "24/7 infrastructure monitoring", "Firewall & network management",
      "Backup & disaster recovery", "Priority response SLA"], True),
    ("Enterprise", "enterprise", "For multi-site or compliance-driven organizations.", None, True,
     ["Unlimited devices", "Dedicated account engineer", "Cybersecurity program & audits",
      "Cloud & server architecture", "Custom SLA & reporting"], False),
]

FAQS = [
    ("What is Managed IT?",
     "Managed IT means NYRIXTECH acts as your outsourced IT department — handling support, infrastructure, "
     "security and monitoring on an ongoing basis for a predictable monthly fee, instead of you calling someone "
     "only when something breaks."),
    ("Who is NYRIXTECH for?",
     "Businesses with roughly 5 to 200 employees that need dependable IT infrastructure but don't need, or can't "
     "yet justify, a full internal IT department — offices, retail, restaurants, hotels, clinics, manufacturing, "
     "logistics and professional services."),
    ("Do you support small businesses?",
     "Yes — many of our clients are small offices with just a handful of employees. Plans and scope are sized to "
     "fit, not a one-size-fits-all enterprise package."),
    ("Can you manage an existing infrastructure, or do we need to start over?",
     "We can take over management of your existing setup in most cases. The free IT audit tells us what's there "
     "and what, if anything, needs to change — we don't assume a rebuild is necessary."),
    ("Can you work with MikroTik?",
     "Yes, MikroTik is one of the network platforms we work with regularly, alongside Cisco and Fortinet."),
    ("Do you support Linux and Windows servers?",
     "Yes, we administer both Windows Server and Linux environments, including mixed setups."),
    ("How does the IT audit work?",
     "We review your network, servers, backup and security setup remotely or on-site, then send you a clear "
     "report of risks and recommendations — no obligation to continue."),
    ("Can you provide remote support?",
     "Yes, most support is delivered remotely, with on-site visits when a hands-on issue requires it."),
    ("Do you provide cybersecurity services?",
     "Yes — firewall management, endpoint protection, access control, security monitoring and incident response "
     "readiness are all part of what we offer, either standalone or as part of Managed IT."),
    ("Do you offer monthly contracts?",
     "Yes, Managed IT is typically delivered as a monthly plan — see Pricing for the available tiers, or contact "
     "us for a tailored plan."),
    ("Can you work alongside an internal IT employee?",
     "Yes, we frequently work alongside an internal employee, handling the workload, coverage and specialist "
     "areas they don't have time or expertise for."),
    ("Can you take over from our current IT provider?",
     "Yes, we regularly onboard companies switching providers. We handle the transition and documentation."),
    ("Is support available outside business hours?",
     "Business and Enterprise plans include 24/7 monitoring with priority response SLAs for critical issues."),
]

CASE_STUDIES = [
    ("Secure Network Infrastructure for Retail", "retail-network-infrastructure", "Retail",
     "Segmented network, MikroTik routing and Wi-Fi redesign across multiple store locations.",
     "This is an illustrative reference scenario showing the type of network infrastructure project NYRIXTECH "
     "delivers for multi-location retail businesses. It does not represent a real client engagement.\n\n"
     "Scenario: A multi-location retail business runs point-of-sale, back-office systems and guest Wi-Fi on a "
     "single flat network with no segmentation, and inconsistent Wi-Fi coverage across stores.\n\n"
     "Approach: Deploy MikroTik routing at each location, segment POS and back-office traffic from guest Wi-Fi "
     "with VLANs, standardize configuration across sites, and set up site-to-site VPN back to a central office "
     "for shared services.\n\n"
     "Outcome: Guest devices can no longer reach business-critical systems, each location is centrally "
     "manageable, and Wi-Fi coverage is consistent store to store."),
    ("Server Monitoring for a Growing Business", "server-monitoring-growing-business", "Professional Services",
     "Zabbix-based monitoring and alerting deployed across a growing on-premise server fleet.",
     "This is an illustrative reference scenario. It does not represent a real client engagement.\n\n"
     "Scenario: A professional services firm's server fleet grew from one to several servers over a few years "
     "with no monitoring in place — issues were only discovered when staff reported something was slow or down.\n\n"
     "Approach: Deploy Zabbix-based monitoring across all servers tracking CPU, RAM, disk and service "
     "availability, tune alert thresholds to avoid noise, and set up a monthly health report.\n\n"
     "Outcome: Disk space and resource issues are flagged with lead time instead of causing outages, and the "
     "business has objective uptime data for the first time."),
    ("VPN Infrastructure for a Distributed Team", "vpn-distributed-team", "Logistics",
     "Site-to-site and remote-access VPN connecting warehouses and a distributed office team.",
     "This is an illustrative reference scenario. It does not represent a real client engagement.\n\n"
     "Scenario: A logistics company operates multiple warehouses plus a distributed office team, previously "
     "coordinating over unsecured remote desktop connections opened directly to the internet.\n\n"
     "Approach: Deploy site-to-site VPN between warehouses and headquarters, set up scoped remote-access VPN for "
     "office staff, and close the exposed remote desktop ports.\n\n"
     "Outcome: All inter-site and remote traffic is encrypted and access-controlled, with no ports directly "
     "exposed to the internet."),
    ("Backup & Disaster Recovery for a Clinic", "backup-disaster-recovery-clinic", "Clinics",
     "Automated, offsite-replicated backup with a tested recovery plan for patient and billing records.",
     "This is an illustrative reference scenario. It does not represent a real client engagement.\n\n"
     "Scenario: A clinic's patient and billing records were backed up to a local external drive only, with no "
     "one verifying the backups actually restored correctly.\n\n"
     "Approach: Implement automated daily backups with offsite replication, define recovery time and recovery "
     "point objectives, and schedule quarterly recovery tests.\n\n"
     "Outcome: Data loss risk from hardware failure or ransomware is substantially reduced, and recovery has "
     "actually been tested and timed rather than assumed to work."),
    ("Segmented Office Network for a Manufacturer", "segmented-office-network-manufacturer", "Manufacturing",
     "VLAN segmentation separating office IT, production systems and guest Wi-Fi on one manufacturing site.",
     "This is an illustrative reference scenario. It does not represent a real client engagement.\n\n"
     "Scenario: A manufacturer ran office computers, production-line equipment and guest Wi-Fi on one flat "
     "network, with no isolation between administrative systems and operational technology.\n\n"
     "Approach: Segment the network into isolated VLANs for office IT, production systems and guest access, "
     "apply firewall rules restricting cross-segment traffic to what's explicitly required, and document the "
     "resulting topology.\n\n"
     "Outcome: A compromised office workstation or guest device can no longer reach production equipment, and "
     "the network is documented for the first time."),
]

BLOG_POSTS = [
    (
        "How to Secure a Small Business Network",
        "how-to-secure-a-small-business-network",
        "Practical, prioritized steps small businesses can take to reduce network security risk.",
        "Most small business networks aren't insecure because of a lack of awareness — they're insecure because "
        "security tasks compete with the daily work of actually running the business, and lose. The good news is "
        "that a handful of prioritized changes cover the majority of the risk.\n\n"
        "Start with the router. Change default admin credentials immediately — routers shipped with guessable "
        "defaults are one of the most common entry points for automated attacks. Disable remote management on "
        "the WAN interface unless you specifically need it, and keep firmware updated.\n\n"
        "Segment your network. A flat network where every device — POS terminals, office computers, guest "
        "laptops and IoT devices — can talk to every other device means a single compromised device puts "
        "everything at risk. Basic VLAN segmentation isolating guest Wi-Fi, IoT devices and business-critical "
        "systems from each other closes off most lateral movement.\n\n"
        "Enforce a real password and access policy. Shared logins with no record of who has access to what make "
        "it impossible to know what happened after an incident, or to revoke access when someone leaves. "
        "Individual accounts, role-based permissions, and removing access promptly when an employee departs are "
        "basic but frequently skipped.\n\n"
        "Patch consistently. Unpatched operating systems and firmware are the single most exploited weakness in "
        "small business networks — not because patches aren't available, but because no one owns the process of "
        "applying them.\n\n"
        "Back up, and verify the backup works. Ransomware turns a missing or untested backup from an "
        "inconvenience into an existential business risk.\n\n"
        "Finally, get a baseline. You can't secure what you haven't assessed. A structured audit of your current "
        "network, access controls and exposure tells you which of the above actually matters most for your "
        "specific setup — which is exactly what a free IT audit is designed to do.",
    ),
    (
        "What Is VLAN and Why Does Your Business Need It?",
        "what-is-vlan-and-why-does-your-business-need-it",
        "A plain-language explanation of network segmentation and when it matters.",
        "VLAN stands for Virtual Local Area Network — a way of splitting one physical network into multiple "
        "logically separate networks, without needing separate physical cabling or switches for each one.\n\n"
        "Without VLANs, every device plugged into your network — or connected to your Wi-Fi — sits on the same "
        "broadcast domain. A guest's laptop, a point-of-sale terminal, a security camera and your accounting "
        "server can all potentially see and talk to each other. That's rarely intentional; it's just what "
        "happens when a network grows organically without anyone designing it.\n\n"
        "VLANs fix this by grouping devices logically instead of physically. A typical small business setup "
        "might use separate VLANs for office workstations, servers, guest Wi-Fi, and any IoT or specialty "
        "devices like cameras or point-of-sale hardware. Traffic between VLANs only flows through a firewall or "
        "router that explicitly allows it — so a compromised guest device or IoT camera can't reach your file "
        "server just because it's plugged into the same building.\n\n"
        "Beyond security, VLANs help with performance and manageability. Separating high-traffic or "
        "broadcast-heavy segments, like a VoIP phone system, from general office traffic reduces congestion, and "
        "having a clear, documented segmentation makes troubleshooting far faster than digging through a flat, "
        "undocumented network.\n\n"
        "Does your business need VLANs? If you have more than a handful of devices, any guest Wi-Fi, IoT "
        "devices, or systems that shouldn't be reachable by everyone on the network — which describes most small "
        "and mid-sized businesses — the answer is almost always yes. It's one of the highest-value, "
        "lowest-disruption changes we implement as part of network infrastructure engagements.",
    ),
    (
        "Why Every Business Needs Reliable Backup",
        "why-every-business-needs-reliable-backup",
        "Backups that have never been tested are not backups. Here's how to do it right.",
        "A backup that has never been tested isn't a backup — it's an assumption. That distinction matters more "
        "than almost anything else in data protection, and it's the single most common gap we find in small "
        "business IT.\n\n"
        "The failure mode is always the same: a backup job was configured at some point, it appears to run, and "
        "nobody has actually tried to restore from it since. Then a server fails, a ransomware attack encrypts "
        "the primary data, or an employee accidentally deletes a shared folder — and the first attempt to "
        "actually use the backup reveals it's corrupted, incomplete, or was never capturing the right data in "
        "the first place.\n\n"
        "A reliable backup strategy has a few non-negotiable components. First, multiple copies — the classic "
        "3-2-1 approach means three copies of your data, on two different types of media, with one copy offsite. "
        "A single backup stored in the same building as the original protects against almost nothing: a fire, "
        "flood or theft takes out both at once.\n\n"
        "Second, automation. Backups that depend on someone remembering to run them manually will eventually be "
        "skipped. Automated, scheduled backups with monitoring and alerting mean a failed backup job gets "
        "flagged the same day, not discovered during an emergency.\n\n"
        "Third — and most overlooked — testing. Recovery time objective (how long can you tolerate being down) "
        "and recovery point objective (how much data can you afford to lose) should be defined upfront, and "
        "recovery should actually be rehearsed on a schedule. A backup you've never restored from is a "
        "hypothesis, not a plan.\n\n"
        "For most small businesses, backup isn't the expensive part of IT — recovering without one is.",
    ),
    (
        "How Server Monitoring Prevents Downtime",
        "how-server-monitoring-prevents-downtime",
        "Why proactive monitoring catches problems before they become outages.",
        "The most common way small businesses find out about a server problem is an employee saying something is "
        "slow or unreachable. By that point, the problem is already affecting the business — and whoever's "
        "troubleshooting is starting from zero, with no history of what led up to it.\n\n"
        "Infrastructure monitoring changes that timeline. Instead of finding out about a full disk when the "
        "server stops accepting new files, monitoring flags the disk crossing a usage threshold days or weeks "
        "earlier, while there's still time to act. Instead of discovering a failed backup job three weeks after "
        "it stopped running, an alert fires the same night.\n\n"
        "Effective monitoring typically tracks a handful of core metrics across your infrastructure: CPU, RAM "
        "and disk utilization; service and application availability; network device status; and backup job "
        "completion. The value isn't in collecting the data — it's in alerting on the right thresholds, tuned to "
        "your specific environment, so real problems stand out instead of getting lost in noise. Poorly tuned "
        "monitoring that fires constantly for non-issues gets ignored, which defeats the purpose entirely.\n\n"
        "Monitoring also builds a historical record. Trend data over weeks and months shows whether resource "
        "usage is climbing steadily — a capacity planning conversation — or spiked suddenly, an incident worth "
        "investigating, which is impossible to reconstruct after the fact without it.\n\n"
        "The business case is straightforward: the cost of monitoring is small and predictable; the cost of "
        "unplanned downtime — lost productivity, missed transactions, emergency support rates — is neither. "
        "Monitoring is what turns IT management from reactive firefighting into something closer to preventive "
        "maintenance.",
    ),
    (
        "MikroTik for Business Networks",
        "mikrotik-for-business-networks",
        "A look at where MikroTik fits for businesses evaluating their next network hardware investment.",
        "MikroTik has become one of the most widely used networking platforms for small and mid-sized "
        "businesses, largely because it offers enterprise-grade routing, firewall and VPN capabilities at a "
        "fraction of the cost of comparable Cisco or Fortinet hardware — without cutting corners on what the "
        "hardware can actually do.\n\n"
        "What makes MikroTik's RouterOS notable is its depth. It supports proper VLAN segmentation, granular "
        "firewall rule sets, site-to-site and remote-access VPN, quality-of-service traffic shaping, and "
        "detailed routing — the same categories of functionality found in higher-priced enterprise gear. The "
        "tradeoff is that RouterOS has a steeper learning curve and a less polished management interface than "
        "some competitors, which is exactly where a lot of small business deployments go wrong: the hardware is "
        "capable, but it's configured with default or minimal settings that leave most of that capability "
        "unused.\n\n"
        "For a growing business, a properly configured MikroTik deployment can cover segmented VLANs isolating "
        "guest, IoT and business-critical traffic; a firewall doing more than just blocking inbound connections; "
        "VPN connecting remote staff or multiple locations securely; and traffic prioritization ensuring VoIP or "
        "point-of-sale traffic isn't starved by a large file transfer.\n\n"
        "MikroTik isn't the only platform worth considering — Cisco and Fortinet remain strong options, "
        "particularly for businesses with existing investment in those ecosystems or specific compliance "
        "requirements. But for businesses evaluating network hardware on a real budget, MikroTik consistently "
        "offers a strong ratio of capability to cost, provided it's actually configured to use that capability "
        "rather than left on defaults.",
    ),
    (
        "How to Build Secure Remote Access for Employees",
        "how-to-build-secure-remote-access-for-employees",
        "VPN, multi-factor authentication and policy considerations for distributed teams.",
        "Remote and hybrid work didn't go away once offices reopened, and neither did the security shortcuts "
        "many businesses adopted to make it work quickly. The most common one — and the riskiest — is exposing a "
        "Remote Desktop Protocol port directly to the internet so employees can connect to their office PC from "
        "home. It's convenient, and it's one of the most heavily targeted entry points for automated attacks and "
        "ransomware.\n\n"
        "Secure remote access starts with a VPN. A properly configured VPN creates an encrypted tunnel into your "
        "network, so remote traffic is protected and — critically — nothing is directly exposed to the open "
        "internet. Remote-access VPN should be scoped per user or group to only what they actually need, not "
        "open access to the entire network; an employee working from home doesn't need direct access to systems "
        "outside their role.\n\n"
        "Multi-factor authentication should sit on top of VPN and any other externally reachable service. A "
        "password alone — especially one reused across services — is not sufficient protection for remote access "
        "to business systems; MFA closes the gap when credentials are inevitably phished or leaked elsewhere.\n\n"
        "Device posture matters too. A personal laptop with no endpoint protection, an outdated OS, and "
        "unrestricted local admin access is a weak link even behind a VPN. At minimum, remote-access devices "
        "should run current endpoint protection and receive security updates.\n\n"
        "Finally, document who has remote access to what, and review it periodically — especially after someone "
        "changes roles or leaves the company. Access that was appropriate a year ago often isn't today, and "
        "unreviewed access is one of the quiet risks that accumulates in every growing business.\n\n"
        "Done properly, remote access doesn't have to be a tradeoff between convenience and security — it's a "
        "configuration problem, not an unsolvable one.",
    ),
    (
        "IT Outsourcing vs Hiring an Internal IT Team",
        "it-outsourcing-vs-hiring-an-internal-it-team",
        "How to think about the tradeoffs between managed IT and building an in-house department.",
        "For a business somewhere between 5 and 200 employees, this decision usually comes down to a mismatch "
        "between what IT actually requires and what a single hire can realistically cover.\n\n"
        "A full internal IT function needs coverage across several distinct areas: help desk support, network "
        "administration, server management, security, backup and monitoring, and vendor management. A single "
        "internal IT hire is rarely deeply skilled in all of these — more commonly, they're strong in one or two "
        "areas and doing their best with the rest. And when that person is sick, on leave, or leaves the company "
        "entirely, coverage drops to zero until a replacement is found and ramped up, often with poor "
        "documentation to work from.\n\n"
        "Hiring a full internal team that covers all of these areas properly is realistic for larger "
        "organizations, but for a growing 20 or 50-person business, the cost — salaries, benefits, training, "
        "redundancy — is usually disproportionate to what's actually needed day to day.\n\n"
        "Outsourced or managed IT addresses this by spreading the same breadth of coverage across a team, for a "
        "predictable monthly cost that scales with your business rather than requiring a large upfront hiring "
        "decision. It also brings documented processes and continuity that don't depend on one person's "
        "institutional knowledge.\n\n"
        "The two approaches aren't strictly exclusive. Many businesses run a hybrid model — an internal employee "
        "who understands the day-to-day operations and handles some tasks directly, backed by a managed IT "
        "provider covering specialist areas like security and infrastructure, and providing coverage when the "
        "internal person is unavailable. This is one of the most common setups we work within, and it's usually "
        "the most cost-effective path for a business that has outgrown 'call someone when it breaks' but isn't "
        "yet the size where a full internal department makes financial sense.\n\n"
        "The right answer depends on your size, growth trajectory and how mission-critical uninterrupted IT "
        "operation is to your business — not a one-size-fits-all rule.",
    ),
    (
        "What Should a Small Business IT Audit Include?",
        "what-should-a-small-business-it-audit-include",
        "A breakdown of what a proper infrastructure audit actually covers.",
        "An IT audit is only useful if it actually reflects how your business runs — a generic checklist tells "
        "you little. Here's what a proper audit should cover, and why each part matters.\n\n"
        "Network infrastructure: what hardware is in place, how it's configured, whether there's any "
        "segmentation between guest, IoT and business-critical traffic, and whether Wi-Fi coverage and firewall "
        "rules match what the business actually needs.\n\n"
        "Servers and core systems: an inventory of what's running, on what hardware, how old it is, and whether "
        "it's still receiving security patches. It's common to find a server running an end-of-life operating "
        "system that nobody flagged as a risk simply because it 'still works.'\n\n"
        "Backup and recovery: not just whether backups are configured, but whether they're actually being "
        "verified, how they're stored — including whether a copy exists offsite — and, critically, whether "
        "recovery has ever been tested.\n\n"
        "Security posture: firewall configuration, endpoint protection coverage, access control (who has access "
        "to what, and whether departed employees still have active accounts), and password policy.\n\n"
        "Monitoring and visibility: whether anyone would actually know if a server went down, a disk filled up, "
        "or a backup failed, before an employee noticed something was broken.\n\n"
        "Documentation: whether the current setup is documented anywhere at all, or exists only in one person's "
        "head — internal or external.\n\n"
        "A useful audit produces a prioritized list of what's actually at risk, not just a generic list of best "
        "practices. Some findings will be urgent, like an exposed remote access port or an untested backup; "
        "others will be lower priority. The goal is a clear picture of where you stand and what to fix first — "
        "which is exactly the format our free IT audit is built around, with no obligation to act on it through "
        "us.",
    ),
    (
        "Common Cybersecurity Mistakes in Small Businesses",
        "common-cybersecurity-mistakes-in-small-businesses",
        "The basic, avoidable gaps behind most small business security incidents.",
        "Most small business security incidents don't involve sophisticated attacks — they involve a handful of "
        "basic gaps that are easy to overlook when IT isn't anyone's full-time focus.\n\n"
        "Default or shared credentials. Routers, switches and admin panels left on factory-default logins, or a "
        "single shared password used across multiple systems and multiple employees, mean there's no way to "
        "know who actually did what, and a single leaked password compromises everything it was reused on.\n\n"
        "No access control discipline. Every employee having full access to every system — rather than access "
        "scoped to what their role actually requires — turns a single compromised account into a much bigger "
        "problem than it needs to be. This is especially risky when former employees' accounts are never "
        "disabled.\n\n"
        "Unpatched systems. Operating systems, firmware and applications that don't get updated regularly are "
        "the most commonly exploited weakness in small business networks — not because attackers are "
        "sophisticated, but because unpatched, known vulnerabilities are the easiest way in.\n\n"
        "No real backup strategy. Covered in more depth elsewhere, but worth repeating: an untested or "
        "single-copy backup turns a ransomware incident from a recoverable event into a potential "
        "business-ending one.\n\n"
        "Flat, unsegmented networks. When a guest device, an IoT camera and the accounting server all sit on the "
        "same network with nothing separating them, a single compromised low-value device becomes a path to "
        "your most sensitive systems.\n\n"
        "No one actually watching. Without monitoring or alerting, most small businesses have no way of knowing "
        "something is wrong until an employee notices, which is often long after the initial compromise.\n\n"
        "None of these require a large security budget to fix — they require someone to own the responsibility "
        "of fixing them. That's the gap a managed IT and cybersecurity partner is designed to close.",
    ),
    (
        "How Much Does IT Support Cost for a Business?",
        "how-much-does-it-support-cost-for-a-business",
        "A grounded look at the real cost comparison between ad-hoc support, an internal hire and managed IT.",
        "There's no single number that applies to every business, because the honest answer depends on your "
        "size, the complexity of your infrastructure, and how much risk you're comfortable carrying — but it's "
        "worth understanding the real cost comparison, not just the sticker price of a monthly plan.\n\n"
        "Ad-hoc support — calling someone only when something breaks — often looks cheapest on paper, because "
        "there's no recurring bill. In practice, it tends to be the most expensive option once you account for "
        "downtime while waiting for someone available, emergency call-out rates, and the absence of any "
        "proactive work, like monitoring, patching or backup verification, that would have prevented the issue "
        "in the first place.\n\n"
        "A single internal IT hire has a predictable salary cost, but represents a single point of failure — no "
        "coverage when they're out, and a skill set that rarely spans networking, security, servers and support "
        "equally well.\n\n"
        "Managed IT plans are typically structured in tiers based on device count, scope of coverage and "
        "response time SLA — a starter tier for a small office with basic support and monitoring, a mid tier "
        "adding 24/7 monitoring and priority response for growing businesses, and custom enterprise pricing for "
        "larger or compliance-driven organizations. Because scope is defined upfront, cost is predictable month "
        "to month rather than spiking during a crisis.\n\n"
        "The honest way to figure out what your business should be spending is to start from what's actually at "
        "risk: how much does an hour of downtime cost you, what would a data loss incident cost to recover from "
        "or explain to customers, and how much of your team's time is currently lost to IT problems that go "
        "unaddressed. A free IT audit is a useful starting point precisely because it grounds the pricing "
        "conversation in your actual infrastructure and risk, not a generic package — see our Pricing page for "
        "indicative plan tiers, or get in touch for a tailored quote.",
    ),
]


class Command(BaseCommand):
    help = "Seed demo content: services, pricing plans, FAQs, case studies, blog posts."

    def handle(self, *args, **options):
        for i, (name, slug, icon, short_desc, features) in enumerate(SERVICES):
            Service.objects.update_or_create(
                slug=slug,
                defaults=dict(
                    name=name, icon=icon, short_description=short_desc,
                    description=short_desc, features=features, order=i,
                ),
            )
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(SERVICES)} services"))

        for i, (name, slug, tagline, price, custom, features, featured) in enumerate(PLANS):
            ServicePlan.objects.update_or_create(
                slug=slug,
                defaults=dict(
                    name=name, tagline=tagline, monthly_price=price, is_custom_pricing=custom,
                    features=features, is_featured=featured, order=i,
                ),
            )
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(PLANS)} pricing plans"))

        for i, (q, a) in enumerate(FAQS):
            FAQ.objects.update_or_create(question=q, defaults=dict(answer=a, order=i))
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(FAQS)} FAQs"))

        for title, slug, industry, summary, content in CASE_STUDIES:
            CaseStudy.objects.update_or_create(
                slug=slug, defaults=dict(title=title, industry=industry, summary=summary, content=content, is_demo=True)
            )
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(CASE_STUDIES)} case studies"))

        category, _ = BlogCategory.objects.get_or_create(slug="it-guides", defaults={"name": "IT Guides"})
        for title, slug, excerpt, content in BLOG_POSTS:
            BlogPost.objects.update_or_create(
                slug=slug,
                defaults=dict(
                    title=title, excerpt=excerpt, content=content, category=category, published=True,
                ),
            )
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(BLOG_POSTS)} blog posts"))

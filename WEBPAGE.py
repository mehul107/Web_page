import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="AWS Cloud Services Hub",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for AWS Branding (Dark Navy & Orange Accents)
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #232F3E 0%, #37475A 100%);
        color: #FFFFFF;
        padding: 2rem;
        border-radius: 12px;
        border-left: 8px solid #FF9900;
        margin-bottom: 1.5rem;
    }
    .service-card {
        background-color: #f8f9fa;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #FF9900;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        color: #1e293b;
    }
    .badge {
        background-color: #232F3E;
        color: #FF9900;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Comprehensive AWS Services Dataset
AWS_DATA = [
    {
        "Category": "Compute",
        "Service": "Amazon EC2 (Elastic Compute Cloud)",
        "Tier": "IaaS",
        "Free_Tier": "750 hrs/mo (t2.micro / t3.micro for 12 months)",
        "Summary": "Secure, resizable virtual machines in the cloud.",
        "Use_Cases": "Web servers, enterprise applications, high-performance computing, batch processing.",
        "Pricing": "Pay-as-you-go per second/hour, Savings Plans, or up to 90% off with Spot Instances.",
        "CLI_Example": "aws ec2 run-instances --image-id ami-0abcdef1234567890 --instance-type t3.micro"
    },
    {
        "Category": "Compute",
        "Service": "AWS Lambda",
        "Tier": "Serverless / FaaS",
        "Free_Tier": "1 Million free requests & 400,000 GB-seconds per month (Always Free)",
        "Summary": "Run code without provisioning or managing servers in response to events.",
        "Use_Cases": "Real-time file processing, serverless APIs (with API Gateway), cron jobs, IoT data ingestion.",
        "Pricing": "Charged based on number of invocations and execution duration in milliseconds.",
        "CLI_Example": "aws lambda invoke --function-name my-function response.json"
    },
    {
        "Category": "Compute",
        "Service": "Amazon ECS & EKS",
        "Tier": "Container Orchestration",
        "Free_Tier": "ECS control plane is free; pay only for underlying EC2/Fargate resources",
        "Summary": "Fully managed container orchestration for Docker (ECS) and Kubernetes (EKS).",
        "Use_Cases": "Microservices architecture, CI/CD containerized deployments, hybrid cloud portability.",
        "Pricing": "ECS is free (pay for compute); EKS costs $0.10/hour per cluster plus compute.",
        "CLI_Example": "aws ecs list-clusters"
    },
    {
        "Category": "Storage",
        "Service": "Amazon S3 (Simple Storage Service)",
        "Tier": "Object Storage",
        "Free_Tier": "5 GB Standard Storage, 20,000 GET & 2,000 PUT requests (12 months)",
        "Summary": "Object storage built to retrieve any amount of data from anywhere with 11 9s durability.",
        "Use_Cases": "Data lakes, static website hosting, software distribution, cloud-native backups.",
        "Pricing": "Tiered per GB/month (Standard, Intelligent-Tiering, Infrequent Access, Glacier).",
        "CLI_Example": "aws s3 cp my-local-file.txt s3://my-bucket-name/"
    },
    {
        "Category": "Storage",
        "Service": "Amazon EBS (Elastic Block Store)",
        "Tier": "Block Storage",
        "Free_Tier": "30 GB of General Purpose (SSD) or Magnetic storage (12 months)",
        "Summary": "High-performance block-level storage volumes designed for use with EC2 instances.",
        "Use_Cases": "Boot volumes for EC2, relational and NoSQL database storage, enterprise throughput apps.",
        "Pricing": "Provisioned GB per month plus provisioned IOPS/throughput depending on volume type (gp3, io2).",
        "CLI_Example": "aws ec2 create-volume --volume-type gp3 --size 80 --availability-zone ap-south-1a"
    },
    {
        "Category": "Databases",
        "Service": "Amazon RDS (Relational Database Service)",
        "Tier": "Managed PaaS",
        "Free_Tier": "750 hrs/mo db.t2.micro/t3.micro/t4g.micro + 20 GB storage (12 months)",
        "Summary": "Set up, operate, and scale relational databases (PostgreSQL, MySQL, Aurora, Oracle, SQL Server).",
        "Use_Cases": "Transactional systems, CRM/ERP platforms, structured web & mobile backends.",
        "Pricing": "Per instance-hour running + provisioned storage (GB/month) + I/O requests.",
        "CLI_Example": "aws rds describe-db-instances"
    },
    {
        "Category": "Databases",
        "Service": "Amazon DynamoDB",
        "Tier": "Serverless NoSQL",
        "Free_Tier": "25 GB storage + 25 Write & 25 Read Capacity Units (Always Free)",
        "Summary": "Fast, flexible NoSQL key-value and document database with single-digit millisecond performance.",
        "Use_Cases": "Real-time bidding, shopping carts, gaming session states, high-velocity IoT telemetry logs.",
        "Pricing": "On-Demand (per million read/write units) or Provisioned capacity mode.",
        "CLI_Example": "aws dynamodb list-tables"
    },
    {
        "Category": "Networking & Content Delivery",
        "Service": "Amazon VPC (Virtual Private Cloud)",
        "Tier": "Network Infrastructure",
        "Free_Tier": "Core VPC, subnets, security groups, and route tables are free",
        "Summary": "Define and launch AWS resources in a logically isolated virtual network that you control.",
        "Use_Cases": "Multi-tier network segmentation (public web subnets vs. private DB subnets), hybrid VPNs.",
        "Pricing": "Free for VPC creation; hourly and data processing charges apply for NAT Gateways & VPNs.",
        "CLI_Example": "aws ec2 create-vpc --cidr-block 10.0.0.0/16"
    },
    {
        "Category": "Networking & Content Delivery",
        "Service": "Amazon CloudFront",
        "Tier": "Global CDN",
        "Free_Tier": "1 TB data transfer out & 10,000,000 HTTP/HTTPS requests per month (Always Free)",
        "Summary": "Fast content delivery network service that securely delivers data, videos, and APIs globally.",
        "Use_Cases": "Caching static web assets at edge locations, DDoS mitigation (with AWS Shield), video streaming.",
        "Pricing": "Per GB of data transferred out to the internet + request counts.",
        "CLI_Example": "aws cloudfront list-distributions"
    },
    {
        "Category": "AI & Machine Learning",
        "Service": "Amazon Bedrock",
        "Tier": "Serverless GenAI",
        "Free_Tier": "Pay-per-use (free trial credits available via AWS events/programs)",
        "Summary": "Build and scale generative AI applications with foundation models via a unified API.",
        "Use_Cases": "Enterprise RAG chatbots, text summarization, code generation, multi-step AI agents.",
        "Pricing": "On-Demand pricing per 1,000 input/output tokens or Provisioned Throughput.",
        "CLI_Example": "aws bedrock list-foundation-models --region us-east-1"
    },
    {
        "Category": "AI & Machine Learning",
        "Service": "Amazon SageMaker",
        "Tier": "Managed ML Platform",
        "Free_Tier": "250 hrs/mo Studio notebooks + 50 hrs/mo training (first 2 months)",
        "Summary": "Build, train, and deploy machine learning models for any use case with fully managed infrastructure.",
        "Use_Cases": "Fraud detection, demand forecasting, custom LLM fine-tuning, computer vision pipelines.",
        "Pricing": "Billed per second for compute, storage, and data processing instances used.",
        "CLI_Example": "aws sagemaker list-endpoints"
    },
    {
        "Category": "Security & Governance",
        "Service": "AWS IAM (Identity & Access Management)",
        "Tier": "Security Core",
        "Free_Tier": "Always Free at no additional charge",
        "Summary": "Securely manage identities, roles, and granular permissions for AWS services and resources.",
        "Use_Cases": "Role-based access control (RBAC), temporary credentials for EC2/Lambda, SSO federation.",
        "Pricing": "Free.",
        "CLI_Example": "aws iam list-roles"
    },
    {
        "Category": "IoT & Edge",
        "Service": "AWS IoT Core",
        "Tier": "Managed IoT Broker",
        "Free_Tier": "250,000 messages/month + 500,000 connection minutes (12 months)",
        "Summary": "Connect billions of IoT devices and route trillions of messages to AWS endpoints without managing servers.",
        "Use_Cases": "Smart agriculture sensor networks, industrial telemetry, connected vehicle fleets.",
        "Pricing": "Charged independently for connectivity, messaging, device shadow, and rules engine usage.",
        "CLI_Example": "aws iot list-things"
    }
]

df = pd.DataFrame(AWS_DATA)

# 4. Header Section
st.markdown("""
    <div class="main-header">
        <h1>☁️ AWS Cloud Services Knowledge Hub</h1>
        <p>Complete reference guide for Amazon Web Services: Compute, Storage, Databases, Networking, AI/ML, Security, and IoT.</p>
    </div>
""", unsafe_allow_html=True)

# 5. Top-Level Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total AWS Services", "240+", "Global Cloud Leader")
col2.metric("Geographic Regions", "34", "108 Availability Zones")
col3.metric("Core Categories Covered", f"{df['Category'].nunique()}", f"{len(df)} Deep-Dive Modules")
col4.metric("Free Tier Eligible", "100+ Services", "12-Month & Always Free")

st.divider()

# 6. Sidebar Navigation & Filtering
st.sidebar.header("🔍 Filter AWS Catalog")
search_query = st.sidebar.text_input("Search by keyword (e.g., serverless, SQL, IoT):", "")
categories = ["All Categories"] + sorted(df["Category"].unique().tolist())
selected_category = st.sidebar.selectbox("Select Service Category:", categories)

st.sidebar.divider()
st.sidebar.markdown("### 💡 Quick AWS Pillars")
st.sidebar.info(
    "**6 Pillars of the AWS Well-Architected Framework:**\n"
    "1. Operational Excellence\n"
    "2. Security\n"
    "3. Reliability\n"
    "4. Performance Efficiency\n"
    "5. Cost Optimization\n"
    "6. Sustainability"
)

# Filter Logic
filtered_df = df.copy()
if selected_category != "All Categories":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if search_query:
    mask = (
        filtered_df["Service"].str.contains(search_query, case=False) |
        filtered_df["Summary"].str.contains(search_query, case=False) |
        filtered_df["Use_Cases"].str.contains(search_query, case=False) |
        filtered_df["Tier"].str.contains(search_query, case=False)
    )
    filtered_df = filtered_df[mask]

# 7. Main Content Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📚 Service Directory",
    "📊 Comparison Matrix",
    "🏗️ Architecture Recommender",
    "🧮 Cost Estimator"
])

# TAB 1: Interactive Service Cards
with tab1:
    st.subheader(f"Showing {len(filtered_df)} AWS Services")
    if filtered_df.empty:
        st.warning("No services matched your search criteria. Try clearing the search bar.")
    else:
        for _, row in filtered_df.iterrows():
            st.markdown(f"""
                <div class="service-card">
                    <span class="badge">{row['Category']} • {row['Tier']}</span>
                    <h3 style="margin-top: 0.5rem; margin-bottom: 0.25rem;">{row['Service']}</h3>
                    <p style="margin-bottom: 0.5rem;"><strong>Overview:</strong> {row['Summary']}</p>
                    <p style="margin-bottom: 0.5rem;"><strong>🎯 Common Use Cases:</strong> {row['Use_Cases']}</p>
                    <p style="margin-bottom: 0.5rem;"><strong>🎁 AWS Free Tier:</strong> {row['Free_Tier']}</p>
                    <p style="margin-bottom: 0;"><strong>💳 Pricing Model:</strong> {row['Pricing']}</p>
                </div>
            """, unsafe_allow_html=True)
            with st.expander(f"💻 View AWS CLI Command for {row['Service']}"):
                st.code(row["CLI_Example"], language="bash")

# TAB 2: Full Data Table & CSV Export
with tab2:
    st.subheader("Full AWS Services Comparison Table")
    st.dataframe(
        filtered_df[["Category", "Service", "Tier", "Free_Tier", "Use_Cases", "Pricing"]],
        use_container_width=True,
        hide_index=True
    )
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered AWS Catalog as CSV",
        data=csv_data,
        file_name="aws_cloud_services_catalog.csv",
        mime="text/csv"
    )

# TAB 3: Architecture Recommender
with tab3:
    st.subheader("🏗️ AWS Reference Architecture Blueprint Finder")
    project_type = st.selectbox(
        "What type of project are you building?",
        [
            "1. Serverless Web Application / REST API",
            "2. IoT Sensor Telemetry & Real-Time Alerting",
            "3. Generative AI Chatbot (RAG Pipeline)",
            "4. Traditional 3-Tier Enterprise Web App"
        ]
    )

    if "1." in project_type:
        st.success("**Recommended Stack:** Amazon CloudFront + Amazon S3 (Frontend) ➔ Amazon API Gateway ➔ AWS Lambda (Compute) ➔ Amazon DynamoDB (NoSQL Database)")
        st.markdown("- **Why this works:** Zero server maintenance, scales to zero when idle, and stays almost entirely within the **Always Free** tier for student/prototype traffic.")
    elif "2." in project_type:
        st.success("**Recommended Stack:** Hardware Node (MQTT) ➔ AWS IoT Core ➔ AWS Lambda ➔ Amazon Timestream / DynamoDB ➔ Amazon SNS (SMS/Email Alerts)")
        st.markdown("- **Why this works:** Decouples edge microcontrollers from cloud storage while enabling instant rule-based triggers for anomalies.")
    elif "3." in project_type:
        st.success("**Recommended Stack:** Streamlit / Next.js UI ➔ AWS Lambda ➔ Amazon Bedrock (Claude / Titan) + Amazon S3 & OpenSearch Serverless (Vector Knowledge Base)")
        st.markdown("- **Why this works:** Eliminates hosting dedicated GPU instances; you pay strictly per token processed.")
    else:
        st.success("**Recommended Stack:** Amazon Route 53 ➔ Application Load Balancer (ALB) ➔ Amazon EC2 Auto Scaling Group (VPC Public/Private Subnets) ➔ Amazon RDS Multi-AZ")
        st.markdown("- **Why this works:** High availability across multiple Availability Zones with strict network isolation for relational databases.")

# TAB 4: Quick Monthly Cost Estimator
with tab4:
    st.subheader("🧮 Interactive Basic AWS Monthly Cost Calculator")
    st.caption("Estimate baseline monthly on-demand costs (US-East / AP-South approximations).")

    c1, c2, c3 = st.columns(3)
    with c1:
        ec2_instances = st.number_input("Number of t3.micro EC2 Instances", min_value=0, max_value=50, value=1)
        ec2_hours = st.slider("Hours running per month", 0, 730, 730)
    with c2:
        s3_gb = st.slider("Amazon S3 Standard Storage (GB)", 0, 5000, 50)
    with c3:
        lambda_reqs = st.number_input("AWS Lambda Requests (in Millions)", min_value=0.0, max_value=100.0, value=1.0, step=0.5)

    # Approximate calculations
    ec2_cost = ec2_instances * ec2_hours * 0.0104
    s3_cost = s3_gb * 0.023
    lambda_cost = max(0.0, (lambda_reqs - 1.0)) * 0.20  # First 1M requests free
    total_cost = ec2_cost + s3_cost + lambda_cost

    st.markdown(f"### Estimated Monthly Total: **${total_cost:,.2f} / month**")
    st.write(f"- **EC2 Compute:** ${ec2_cost:,.2f} | **S3 Storage:** ${s3_cost:,.2f} | **Lambda Serverless:** ${lambda_cost:,.2f}")
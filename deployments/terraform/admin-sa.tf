resource "kubernetes_service_account" "cluster-admin" {
  provider = "kubernetes.primary"
  metadata {
    name = "cluster-admin"
    namespace = "kube-system"
  }
}

data "kubernetes_secret" "cluster-admin-token" {
  provider = "kubernetes.primary"
  metadata {
    name = "${kubernetes_service_account.cluster-admin.default_secret_name}"
    namespace = "${kubernetes_service_account.cluster-admin.metadata.0.namespace}"
  }

  depends_on = [kubernetes_service_account.cluster-admin]
}

resource "kubernetes_cluster_role_binding" "cluster-admin-binding" {
  provider = "kubernetes.primary"
  metadata {
    name = "cluster-admin-binding"
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = "cluster-admin"
  }

  subject {
    kind      = "ServiceAccount"
    name      = "${kubernetes_service_account.cluster-admin.metadata.0.name}"
    namespace = "kube-system"
  }
}
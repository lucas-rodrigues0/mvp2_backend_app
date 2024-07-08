articles_query = """
    query {
        articles {
            articleId
            title
            content
            userNickname
            updatedAt
            comments {
                commentId
                content
                userNickname
                updatedAt
                replies {
                    commentId
                    content
                    userNickname
                    updatedAt
                }
            }
        }
    }
"""

article_by_id_query = """
    query ($articleID: UUID!) {
        articleById(articleId: $articleID) {
            title
            content
            userNickname
            updatedAt
            comments {
                commentId
                content
                updatedAt
                userNickname
                replies {
                    commentId
                    content
                    updatedAt
                    userNickname
                }
            }
        }
    }
"""

articles_by_user_id_query = """
    query ($userID: String!) {
        articlesByUserId(userId: $userID) {
            articleId
            title
            content
            userNickname
            updatedAt
            comments {
                commentId
                content
                userNickname
                updatedAt
                replies {
                    commentId
                    content
                    userNickname
                    updatedAt
                }
            }
        }
    }
"""

articles_by_period_query = """
    query ($endDate: String!, $initialDate: String!) {
        articlesByPeriod(
            endDate: $endDate,
            initialDate: $initialDate
        ) {
            articleId
            title
            content
            userNickname
            updatedAt
            comments {
                commentId
                content
                userNickname
                updatedAt
                replies {
                    commentId
                    content
                    userNickname
                    updatedAt
                }
            }
        }
    }
"""

add_article_mutation = """
    mutation (
        $content: String!,
        $title: String!,
        $userEmail: String!,
        $userID: String!,
        $userNickname: String!
    ) {
        addArticle(
            content: $content,
            title: $title,
            userEmail: $userEmail,
            userId: $userID,
            userNickname: $userNickname
        ) {
            ... on AddArticle {
                articleId
                title
                userNickname
            }
            ... on UserInfoMissing {
                errors
            }
            ... on ArticleContentMissing {
                errors
            }
        }
    }
"""

remove_article_mutation = """
    mutation ($articleID: UUID!, $userID: String!) {
        removeArticle(articleId: $articleID, userId: $userID) {
            ... on ArticleDeleted {
                message
            }
            ... on InvalidUser {
                errors
            }
        }
    }
"""

update_article_mutation = """
    mutation (
        $articleID: UUID!,
        $content: String = null,
        $title: String = null,
        $userID: String!,
    ) {
        updateArticle(
            articleId: $articleID,
            userId: $userID,
            content: $content,
            title: $title
        ) {
            ... on AddArticle {
                articleId
                content
                title
                updatedAt
                userNickname
            }
            ... on InvalidUser {
                errors
            }
        }
    }
"""

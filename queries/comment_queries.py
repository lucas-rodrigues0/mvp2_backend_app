comments_query = """
    query {
        comments {
            commentId
            isReply
            commentReply
            content
            userNickname
            updatedAt
            articleId
            replies {
                commentId
                isReply
                commentReply
                content
                userNickname
                updatedAt
            }
        }
    }
"""

comment_by_id_query = """
    query ($commentID: UUID!) {
        commentById(commentId: $commentID) {
            commentId
            articleId
            content
            commentReply
            isReply
            userNickname
            updatedAt
        }
    }
"""

comments_by_user_id_query = """
    query ($userID: String!) {
        commentByUserId(userId: $userID) {
            commentId
            articleId
            isReply
            commentReply
            content
            userNickname
            updatedAt
        }
    }
"""

comments_by_period_query = """
    query ($endDate: String!, $initialDate: String!) {
        commentsByPeriod(
            endDate: $endDate,
            initialDate: $initialDate
        ) {
            commentId
            articleId
            isReply
            commentReply
            content
            userNickname
            updatedAt
            replies {
                commentId
                isReply
                commentReply
                content
                userNickname
                updatedAt
            }
        }
    }
"""

add_comment_mutation = """
    mutation (
        $articleID: UUID!,
        $commentReply: UUID = null,
        $content: String!,
        $isReply: Boolean = false,
        $userEmail: String!,
        $userID: String!,
        $userNickname: String!,
    ) {
        addComment(
            articleId: $articleID,
            commentReply: $commentReply,
            content: $content,
            isReply: $isReply,
            userEmail: $userEmail,
            userId: $userID,
            userNickname: $userNickname,
        ) {
            ... on AddComment {
                articleId
                isReply
                commentReply
                commentId
                content
                userNickname
            }
            ... on UserInfoMissing {
                errors
            }
            ... on CommentReplyNotAllowed {
                errors
            }
            ... on CommentContentMissing {
                errors
            }
        }
    }
"""

remove_comment_mutation = """
    mutation ($commentID: UUID!, $userID: String!) {
        removeComment(commentId: $commentID, userId: $userID) {
            ... on CommentDeleted {
                message
            }
            ... on InvalidUser {
                errors
            }
        }
    }
"""

update_comment_mutation = """
    mutation (
        $commentID: UUID!,
        $content: String!,
        $userID: String!,
    ) {
        updateComment(
            commentId: $commentID,
            content: $content,
            userId: $userID
        ) {
            ... on AddComment {
                articleId
                commentId
                isReply
                commentReply
                content
                userNickname
            }
            ... on CommentContentMissing {
                errors
            }
            ... on InvalidUser {
                errors
            }
        }
    }
"""

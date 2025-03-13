const functions = require("firebase-functions");
const admin = require("firebase-admin");
admin.initializeApp();

const db = admin.database();

exports.sendNotifications = functions.database
  .ref("/Posts/{postId}")
  .onCreate(async (snapshot, context) => {
    const post = snapshot.val();
    const { tags, author_id, description, timestamp } = post;

    try {
      const usersSnapshot = await db.ref("/Users").once("value");
      const users = usersSnapshot.val();

      if (!users) {
        console.log("No users found in the database.");
        return null;
      }

      const notifications = {};

      for (const userId in users) {
        const user = users[userId];

        // Check if the user follows the author or any tags
        const followsAuthor = (user.FollowedUsers || []).includes(author_id);
        const followsTag = (tags || []).some((tag) =>
          (user.UserTags || []).includes(tag)
        );

        if (followsAuthor || followsTag) {
          const notificationId = db.ref().push().key;
          notifications[`/Notifications/${userId}/${notificationId}`] = {
            NotContent: `${author_id} posted: ${description}`,
            NotTags: tags,
            NotTimestamp: timestamp || new Date().toISOString()
          };
        }
      }

      if (Object.keys(notifications).length > 0) {
        await db.ref().update(notifications);
      }
    } catch (error) {
      console.error("Error sending notifications:", error);
    }
    return null;
  });

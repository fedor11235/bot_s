-- CreateTable
CREATE TABLE "PromoCode" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "idUser" TEXT NOT NULL,
    "code" TEXT NOT NULL
);

-- CreateTable
CREATE TABLE "User" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "idUser" TEXT NOT NULL,
    "tariffPlan" TEXT NOT NULL DEFAULT 'base',
    "subscriptionEndDate" TEXT NOT NULL DEFAULT 'never',
    "createdOpt" INTEGER NOT NULL DEFAULT 0,
    "byOpt" INTEGER NOT NULL DEFAULT 0,
    "totalSavings" INTEGER NOT NULL DEFAULT 0,
    "invitedUsers" INTEGER NOT NULL DEFAULT 0,
    "totalEarned" INTEGER NOT NULL DEFAULT 0,
    "channels" INTEGER NOT NULL DEFAULT 0
);

-- CreateTable
CREATE TABLE "UserChanel" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "idUser" TEXT NOT NULL,
    "idChanel" TEXT NOT NULL
);

-- CreateTable
CREATE TABLE "Catalog" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "category" TEXT,
    "username" TEXT,
    "title" TEXT,
    "daily_reach" INTEGER,
    "ci_index" INTEGER,
    "participants_count" INTEGER,
    "avg_post_reach" INTEGER,
    "forwards_count" INTEGER
);

// This file is part of babel4iphone.

// Copyright (C) 2009 Giovanni Amati <amatig@gmail.com>

// babel4iphone is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// babel4iphone is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with babel4iphone.  If not, see <http://www.gnu.org/licenses/>.


#import "CoreFunctions.h"

@implementation CoreFunctions

+(void) dispatch:(NSString *)msg
{
	NSArray *arr = [msg componentsSeparatedByString:@"|"];
	
	// MENU
	if ([[arr objectAtIndex:0] isEqualToString:@"M"])
	{
		NSArray *menuitems = [[arr objectAtIndex:1] componentsSeparatedByString:@";"];
		id interface = [[[CCDirector sharedDirector] runningScene] getChildByTag:1];
		[interface initMenu:menuitems];
		NSLog(@"Menu: %@", [arr objectAtIndex:1]);
	}
	// TURN
	else if ([[arr objectAtIndex:0] isEqualToString:@"T"])
	{
		id interface = [[[CCDirector sharedDirector] runningScene] getChildByTag:1];
		[interface setTurn:[arr objectAtIndex:1]];
		NSLog(@"Turn: %@", [arr objectAtIndex:1]);
	}
	// ANIM FIGHT
	else if ([[arr objectAtIndex:0] isEqualToString:@"A"])
	{
		id game = [[[CCDirector sharedDirector] runningScene] getChildByTag:0];
		[game playFight];
		NSLog(@"play fight: %@", [arr objectAtIndex:1]);
	}
	// CHARACTER
	else if ([[arr objectAtIndex:0] isEqualToString:@"P1"])
	{
		id game = [[[CCDirector sharedDirector] runningScene] getChildByTag:0];
		int pos = 1;
		NSArray *chrs = [[arr objectAtIndex:1] componentsSeparatedByString:@";"];
		for (NSString *c in chrs)
		{
			NSArray *info = [c componentsSeparatedByString:@","];
			[game addMyCharacter:info position:pos];
			pos = pos + 1;
		}
	}
	else if ([[arr objectAtIndex:0] isEqualToString:@"P2"])
	{
		id game = [[[CCDirector sharedDirector] runningScene] getChildByTag:0];
		int pos = 1;
		NSArray *chrs = [[arr objectAtIndex:1] componentsSeparatedByString:@";"];
		for (NSString *c in chrs)
		{
			NSArray *info = [c componentsSeparatedByString:@","];
			[game addEnemyCharacter:info position:pos];
			pos = pos + 1;
		}
	}
	// ECHO
	else if ([[arr objectAtIndex:0] isEqualToString:@"E"])
	{
		UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Alert" message:[arr objectAtIndex:1] delegate:self cancelButtonTitle:@"Cancel" otherButtonTitles:@"Ok", nil];
		[alert show];
		[alert release];
	}
	// NOT IMPLEMENTED
	else
		NSLog(@"Not implemented: %@", arr);
}

+(void) alertView:(UIAlertView *)actionSheet clickedButtonAtIndex:(NSInteger)buttonIndex
{
	// the user clicked one of the OK/Cancel buttons
	if (buttonIndex == 1)
	{
		NSLog(@"Ok on %@", [actionSheet title]);
	}
	else
	{
		NSLog(@"Cancel on %@", [actionSheet title]);
	}
}

+(void) copyDatabaseToDocuments:(NSString *)databasePath named:(NSString *)databaseName
{
	// Create a FileManager object
	NSFileManager *fileManager = [NSFileManager defaultManager];
	// Get the path to the database in the application package
	NSString *databasePathFromApp = [[[NSBundle mainBundle] resourcePath] stringByAppendingPathComponent:databaseName];
	// Check if the database already exists then remove it
	BOOL success = [fileManager fileExistsAtPath:databasePath];
	if (success)
	{
		if ([fileManager contentsEqualAtPath:databasePathFromApp andPath:databasePath] == YES)
			NSLog(@"SQLITE Same database");
		else
		{
			[fileManager removeItemAtPath:databasePath error:nil];
			success = FALSE;
			NSLog(@"SQLITE Remove database");
		}
	}
	if (!success)
	{
		// Copy the database from the package to the users filesystem
		[fileManager copyItemAtPath:databasePathFromApp toPath:databasePath error:nil];
		NSLog(@"SQLITE Copy new database");
	}
	
	[fileManager release];
}

/////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////// CALC UTILITIES /////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////

+(int) scaleHP:(float)sHP baseHP:(float)bHP scaleHPxXx:(float)sHPxXx level:(int)l
{
	float raceHP = sHP * (l-1) + bHP;
	if (l > 10)
		raceHP += 2 * (l-10);
	if (l > 30)
		raceHP += sHPxXx * (l-30);
	return (int)raceHP;
}

+(int) scaleHP:(float)sHP baseHP:(float)bHP scaleHPxXx:(float)sHPxXx level:(int)l job:(NSString *)j
{
	float jobHP = sHP * (l-1) + bHP;
	if (l > 30)
		jobHP += sHPxXx * (l-30);
	if (l >= 15 && [j isEqualToString:@"Monk"])
		jobHP += 30;
	if (l >= 35 && [j isEqualToString:@"Monk"])
		jobHP += 30;
	return (int)jobHP;
}

+(int) scaleHP:(float)sHP baseHP:(float)bHP suplevel:(int)sl supjob:(NSString *)sj
{
	float supjobHP = sHP * (sl-1) + bHP;
	if (sl > 10)
		supjobHP += sl-10;
	supjobHP = supjobHP / 2;
	if (sl >= 15 && [sj isEqualToString:@"Monk"])
		supjobHP += 30;
	if (sl >= 35 && [sj isEqualToString:@"Monk"])
		supjobHP += 30;
	return (int)supjobHP;
}

+(int) scaleMP:(float)sMP baseMP:(float)bMP levelMP:(int)lm
{
	return (int)(sMP * (lm-1) + bMP);
}

+(int) scaleMP:(float)sMP baseMP:(float)bMP levelMP:(int)lm level:(int)l job:(NSString *)j
{
	float jobMP = sMP * (lm-1) + bMP;
	if (l >= 10 && [j isEqualToString:@"Summoner"])
		jobMP += 15;
	if (l >= 30 && [j isEqualToString:@"Summoner"])
		jobMP += 15;
	if (l >= 50 && [j isEqualToString:@"Summoner"])
		jobMP += 10;
	if (l >= 70 && [j isEqualToString:@"Summoner"])
		jobMP += 10;
	return (int)jobMP;
}

+(int) scaleMP:(float)sMP baseMP:(float)bMP suplevel:(int)sl supjob:(NSString *)sj
{
	float supjobMP = (sMP * (sl-1) + bMP) / 2;
	if (sl >= 10 && [sj isEqualToString:@"Summoner"])
		supjobMP += 15;
	if (sl >= 30 && [sj isEqualToString:@"Summoner"])
		supjobMP += 15;
	return (int)supjobMP;
}

+(int) scaleSTATS:(float)sSTATS baseSTATS:(float)bSTATS level:(int)l
{
	return (int)(sSTATS * (l-1) + bSTATS);
}

@end
